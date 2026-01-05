import streamlit as st
import requests
import json
import time
from datetime import datetime, timezone, timedelta

# ===============================
# STREAMLIT CONFIG
# ===============================
st.set_page_config(
    page_title="VID / UID → User Details Fetcher",
    layout="wide",
)

st.title("𝖬𝖺𝗅𝗈𝗇𝖾'𝗌 𝖲𝗎𝗉𝗋𝖾𝗆𝖺𝖼𝗒 👑")
st.caption("Advanced user profile view")

# ===============================
# HARDCODED COOKIE (PRIVATE USE)
# ===============================
UAAS_COOKIE = "SRPGxjh0Fi%2FdhdZI7D%2BOso2CG4l3qqeE5D5ijqQYWv5FD8la3wxUhWICbw2hzZq2%2CnNM9ovMxw6%2FuGyqZkcBz7TGvNU8RVQJRNigKGUsMqsP4Gri%2FdeKtNZMBeVw3gAHwTgajycqZX%2B4UiMpJgZiv7m0Jl8MER8NgstKsx5rhNTE3SaY2bGwcjSeGBG3%2Bq7PzKy87bQ4NmYChYm7%2Fg%2BHEjGvNVyTvbvfCVcnsHNjHCT17FjnStaTTx8i78ZQ2aikQKBLoFJjhWsfJz5EIhcd4C458wRvDVTzLDUG43f7%2BrrsVQeVubF6IVo1kzvRbpnrhGC0ZgQvqLg9KAwzbl0a37UWnK3SSMUYv9Q5nhmsecFjpoKk3h1YMGuG056XYDlhBVqEhrTJIOWfstOdyYi%2FtFp41xQwYLPVlh6vTI2OsDLFKxD%2FjsBmx53qVNNzhhIm0xHJ2E4EicvEJk1yAM%2F4iqRaLTl%2BnPTzX09dcBAfE6PY2gkpe0I7mUc8lKKjJ3J7YLbZ3Hoax1pjGF4wKzx0%2Ff5qwN67ifFOMnFIbKlLZNbFzTJ47M%2BZoIg%3D%3D"

# ===============================
# TIME HELPERS (IST)
# ===============================
IST = timezone(timedelta(hours=5, minutes=30))

def ts():
    return str(int(time.time() * 1000))

def ts_to_ist(ts_val):
    if not ts_val:
        return "-"
    dt = datetime.fromtimestamp(int(ts_val), tz=IST)
    return dt.strftime("%Y-%m-%d %I:%M:%S %p IST")

def days_ago(ts_val):
    if not ts_val:
        return "-"
    now = datetime.now(IST)
    dt = datetime.fromtimestamp(int(ts_val), tz=IST)
    return f"{(now - dt).days} days ago"

def gender(v):
    return {0: "Unknown", 1: "Male", 2: "Female"}.get(v, "Unknown")

# ===============================
# INPUT (ENTER KEY WORKS)
# ===============================
with st.form("fetch_form"):
    user_input = st.text_input(
        "Enter VID or UID",
        placeholder="2077576330 (VID)  |  4466939783 (UID)"
    )
    fetch_btn = st.form_submit_button("🚀 Fetch User Info")

# ===============================
# MAIN LOGIC
# ===============================
if fetch_btn:
    if not user_input.isdigit():
        st.error("❌ Input must be numeric")
    else:
        try:
            uid = None

            # ===============================
            # DETECT UID OR VID
            # ===============================
            if user_input.startswith("4"):
                uid = int(user_input)
                st.success(f"✅ Using direct UID: {uid}")

            else:
                with st.spinner("Resolving VID → UID..."):
                    r1 = requests.post(
                        "https://i-875.olaparty.com/ymicro/api",
                        headers={
                            "X-Ymicro-Api-Method-Name": "InformAgainst.CheckUnsealFriend",
                            "X-Ymicro-Api-Service-Name": "net.ihago.inform.srv.mgr",
                            "Hago-Seq-Id": ts(),
                            "X-Ostype": "android",
                            "X-Os-Ver": "12",
                            "X-App-Ver": "50800",
                            "Content-Type": "application/json",
                        },
                        cookies={"uaasCookie": UAAS_COOKIE},
                        json={
                            "sequence": int(ts()),
                            "vid": int(user_input),
                            "t": 1
                        },
                        timeout=20
                    )

                    uid = r1.json()["user_info"]["uid"]
                    st.success(f"✅ VID resolved → UID: {uid}")

            # ===============================
            # UID → FULL PROFILE
            # ===============================
            with st.spinner("Fetching full user profile..."):
                r2 = requests.post(
                    "https://api.olaparty.com/ymicro/sapi",
                    params={
                        "method": "Uinfo.GetUinfoByVer",
                        "sname": "net.ihago.uinfo.api.uinfo",
                        "_method": "Uinfo.GetUinfoByVer",
                        "hago-seq-id": ts(),
                    },
                    headers={
                        "Content-Type": "text/plain",
                        "X-App-Ver": "10102",
                        "X-Os-Ver": "12",
                        "X-Ostype": "android",
                    },
                    cookies={
                        "uaasCookie": UAAS_COOKIE,
                        "hagouid": str(uid)
                    },
                    data=json.dumps({
                        "sequence": int(ts()),
                        "uids": [{"uid": uid}]
                    }),
                    timeout=20
                )

                data = r2.json()
                info = data["infos"][0]

            # ===============================
            # PROFILE HEADER
            # ===============================
            col1, col2 = st.columns([1, 3])

            with col1:
                avatar_url = info.get("avatar")
                st.image(avatar_url, width=180)
                reg_ts = info.get("register_time")
                st.markdown(
                    f"🕒 **Registered:**  \n"
                    f"{ts_to_ist(reg_ts)}  \n"
                    f"⏳ *{days_ago(reg_ts)}*"
                )
                if avatar_url:
                    st.markdown(f"🔗 [Open Avatar Image]({avatar_url})")

            with col2:
                st.markdown(f"## {info.get('nick')}")
                st.markdown(f"**UID:** `{info.get('uid')}`")
                st.markdown(f"**VID:** `{info.get('vid')}`")
                st.markdown(f"**Gender:** {gender(info.get('sex'))}")
                st.markdown(f"**Birthday:** {info.get('birthday')}")
                st.markdown(f"**Bio:** {info.get('sign')}")

            st.divider()

            # ===============================
            # BASIC INFO
            # ===============================
            st.subheader("📌 Basic Information")
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(f"**🌍 Country:** {info.get('country')}")
                st.markdown(f"**🏳 Region:** {info.get('region')}")
                st.markdown(f"**🏠 Hometown:** {info.get('hometown')}")

            with c2:
                st.markdown(f"**📱 Device:** {info.get('device')}")
                st.markdown(f"**🧠 OS:** {info.get('os_type')}")
                st.markdown(f"**📦 App Name:** {info.get('app_name')}")

            with c3:
                st.markdown(f"**🔢 App Version:** {info.get('app_ver')}")
                st.markdown(f"**🗣 Language:** {info.get('lang')}")
                st.markdown(f"**💼 Job:** {info.get('job')}")

            # ===============================
            # ACTIVITY
            # ===============================
            st.subheader("🕒 Registration & Activity (IST)")
            r1, r2, r3 = st.columns(3)

            with r1:
                st.markdown("**🟢 Register Time**")
                st.write(ts_to_ist(info.get("register_time")))
                st.caption(days_ago(info.get("register_time")))

            with r2:
                st.markdown("**🟢 First Login**")
                st.write(ts_to_ist(info.get("first_login_time")))
                st.caption(days_ago(info.get("first_login_time")))

            with r3:
                st.markdown("**🔵 Last Login**")
                st.write(ts_to_ist(info.get("last_login_time")))
                st.caption(days_ago(info.get("last_login_time")))

            # ===============================
            # VIP / FLAGS
            # ===============================
            st.subheader("⭐ VIP / Flags")
            hago_ext = info.get("hago_ext", {})
            st.markdown(f"**SVIP Level:** {hago_ext.get('svip_level')}")
            st.markdown(f"**Forbid Follow:** {hago_ext.get('forbid_follow')}")
            st.markdown(f"**Forbid Bother:** {hago_ext.get('forbid_bother')}")

            # ===============================
            # LABELS
            # ===============================
            st.subheader("🏷 Labels")
            st.write(info.get("label_ids", []))

            # ===============================
            # RAW JSON
            # ===============================
            with st.expander("🧾 Raw JSON Response"):
                st.json(data)

        except Exception as e:
            st.error(f"🔥 Error occurred: {e}")

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("𝖢𝗋𝖾𝖺𝗍𝖾𝖽 𝖡𝗒 𝖬𝖺𝗅𝗈𝗇𝖾 𝖯𝗏𝗍 𝖮𝗇𝗅𝗒 🔐")
