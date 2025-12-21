import streamlit as st
import requests
import json
import time
from datetime import datetime

# ===============================
# STREAMLIT CONFIG
# ===============================
st.set_page_config(
    page_title="VID → User Details Fetcher",
    layout="wide",
)

st.title("🔍 VID → User Details Fetcher")
st.caption("Advanced profile view from VID")

# ===============================
# HARDCODED COOKIE (PRIVATE REPO ONLY)
# ===============================
UAAS_COOKIE = "wEri87yq01Zzqgf4qSTpmddlv6%2FUCMU2DrLW1yOup21B6kswFTe4f1T0syyzDejl%2CnNM9ovMxw68QzWOyQX236BxhgJK9ffj%2BtHd8YDwrmMCxeHcUP3khT7ZIlfNaJH%2FP555SKvk%2BwkLQR%2BxiNEMh6CqdrdI%2F0YkLLRJALxoBMthSdWByXPACYv1L2RehQk8Gc98I9RIG5h11g87OtUXE4Jymwhxz4Y6RdQEcUpSSuOJq3agxtkoAZ2BZrFdG4SwP6AnYaVtghDNjm8G8g9sGSozagbhZxA%2Fde9IDqORxokDpFmCjcQ%2Fcbzg%2F%2Fb4vHfrrUUAyi83RA7l1%2Brq7LBl9Z2yNrbCpDo2adm0Qk57VVRroC5oEv%2BX8RyddWcupr6QTf0bm9KRuE62pKCkfWC37v9ahvIFOrDcO7EfKH33za5cio4SGTBT6LXU4fpMlvbr48NGLvLPCTDWejlROuPZmTQV6vQXnZe6pAGSJePwpMo0v%2FEzV6CN%2Bm4crHWjw091VHKK5f%2BXaxEyfakeEleUZyaYza8BlqCABfbOrWmDV7DeWAi2NTpSBR%2F%2BEmv9AwzLE"

# ===============================
# HELPERS
# ===============================
def ts():
    return str(int(time.time() * 1000))

def ts_to_date(ts_val):
    if not ts_val:
        return "-"
    return datetime.fromtimestamp(int(ts_val)).strftime("%Y-%m-%d %H:%M:%S")

def gender(val):
    return {0: "Unknown", 1: "Male", 2: "Female"}.get(val, "Unknown")

# ===============================
# INPUT
# ===============================
vid = st.text_input("Enter VID", placeholder="177307453")
fetch_btn = st.button("🚀 Fetch User Info")

# ===============================
# MAIN LOGIC
# ===============================
if fetch_btn:
    if not vid.isdigit():
        st.error("VID must be numeric")
    else:
        try:
            # ===============================
            # 1️⃣ VID → UID
            # ===============================
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
                        "vid": int(vid),
                        "t": 1
                    },
                    timeout=20
                )

                uid = r1.json()["user_info"]["uid"]

            # ===============================
            # 2️⃣ UID → FULL INFO
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
                st.image(info.get("avatar"), width=180)

            with col2:
                st.markdown(f"## {info.get('nick')}")
                st.markdown(f"**UID:** `{info.get('uid')}`")
                st.markdown(f"**VID:** `{info.get('vid')}`")
                st.markdown(f"**Gender:** {gender(info.get('sex'))}")
                st.markdown(f"**Birthday:** {info.get('birthday')}")
                st.markdown(f"**Bio:** {info.get('sign')}")

            st.divider()

            # ===============================
            # BASIC DETAILS
            # ===============================
            st.subheader("📌 Basic Information")
            c1, c2, c3 = st.columns(3)

            c1.write("🌍 Country:", info.get("country"))
            c1.write("🏳 Region:", info.get("region"))
            c1.write("🏠 Hometown:", info.get("hometown"))

            c2.write("📱 Device:", info.get("device"))
            c2.write("🧠 OS:", info.get("os_type"))
            c2.write("📦 App:", info.get("app_name"))

            c3.write("🔢 App Version:", info.get("app_ver"))
            c3.write("🗣 Language:", info.get("lang"))
            c3.write("💼 Job:", info.get("job"))

            # ===============================
            # ACTIVITY
            # ===============================
            st.subheader("⏱ Activity")
            a1, a2, a3 = st.columns(3)

            a1.write("🟢 First Login:", ts_to_date(info.get("first_login_time")))
            a1.write("🟢 Register Time:", ts_to_date(info.get("register_time")))

            a2.write("🔵 Last Login:", ts_to_date(info.get("last_login_time")))
            a2.write("🔵 Last Logout:", ts_to_date(info.get("last_logout_time")))

            a3.write("📡 On Micro:", info.get("on_micro"))
            a3.write("⚠ Status:", info.get("status"))

            # ===============================
            # VIP / FLAGS
            # ===============================
            st.subheader("⭐ VIP / Flags")
            hago_ext = info.get("hago_ext", {})

            st.write("SVIP Level:", hago_ext.get("svip_level"))
            st.write("Anonymous Homepage:", hago_ext.get("anonymous_accessing_homepage"))
            st.write("Forbid Follow:", hago_ext.get("forbid_follow"))
            st.write("Forbid Bother:", hago_ext.get("forbid_bother"))

            # ===============================
            # LABELS
            # ===============================
            st.subheader("🏷 Labels")
            st.write(info.get("label_ids", []))

            # ===============================
            # RAW JSON (OPTIONAL)
            # ===============================
            with st.expander("🧾 Raw JSON Response"):
                st.json(data)

        except Exception as e:
            st.error(f"Error occurred: {e}")

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("⚠️ Advanced profile view | Hardcoded cookie version")
