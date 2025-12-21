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
UAAS_COOKIE = (
    "wEri87yq01Zzqgf4qSTpmddlv6%2FUCMU2DrLW1yOup21B6kswFTe4f1T0syyzDejl%2C"
    "nNM9ovMxw68QzWOyQX236BxhgJK9ffj%2BtHd8YDwrmMCxeHcUP3khT7ZIlfNaJH%2FP555"
    "SKvk%2BwkLQR%2BxiNEMh6CqdrdI%2F0YkLLRJALxoBMthSdWByXPACYv1L2RehQk8Gc98I9"
    "RIG5h11g87OtUXE4Jymwhxz4Y6RdQEcUpSSuOJq3agxtkoAZ2BZrFdG4SwP6AnYaVtgh"
    "DNjm8G8g9sGSozagbhZxA%2Fde9IDqORxokDpFmCjcQ%2Fcbzg%2F%2Fb4vHfrrUUAyi83RA7"
    "l1%2Brq7LBl9Z2yNrbCpDo2adm0Qk57VVRroC5oEv%2BX8RyddWcupr6QTf0bm9KRuE62pK"
    "CkfWC37v9ahvIFOrDcO7EfKH33za5cio4SGTBT6LXU4fpMlvbr48NGLvLPCTDWejlROuP"
    "ZmTQV6vQXnZe6pAGSJePwpMo0v%2FEzV6CN%2Bm4crHWjw091VHKK5f%2BXaxEyfakeEleUZ"
    "yaYza8BlqCABfbOrWmDV7DeWAi2NTpSBR%2F%2BEmv9AwzLE"
)

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
# INPUT (UI IDENTICAL, ENTER WORKS)
# ===============================
with st.form("fetch_form"):
    user_input = st.text_input(
        "Enter VID or UID",
        placeholder="177307453 (VID)  |  4466939783 (UID)"
    )
    fetch_btn = st.form_submit_button("🚀 Fetch User Info")

# ===============================
# MAIN LOGIC (UNCHANGED)
# ===============================
if fetch_btn:
    if not user_input.isdigit():
        st.error("❌ Input must be numeric")
    else:
        try:
            if user_input.startswith("4"):
                uid = int(user_input)
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

            # ⬇️ EVERYTHING BELOW IS EXACTLY AS BEFORE ⬇️
            col1, col2 = st.columns([1, 3])

            with col1:
                st.image(info.get("avatar"), width=180)

            with col2:
                st.markdown(f"## {info.get('nick')}")

            st.divider()

            with st.expander("🧾 Raw JSON Response"):
                st.json(data)

        except Exception as e:
            st.error(f"🔥 Error occurred: {e}")

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("𝖢𝗋𝖾𝖺𝗍𝖾𝖽 𝖡𝗒 𝖬𝖺𝗅𝗈𝗇𝖾 𝖯𝗏𝗍 𝖮𝗇𝗅𝗒 🔐")
