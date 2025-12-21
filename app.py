import streamlit as st
import requests
import json
import time
from datetime import datetime, timezone, timedelta

# ===============================
# STREAMLIT CONFIG
# ===============================
st.set_page_config(
    page_title="VID → User Details Fetcher",
    layout="wide",
)

st.title("🔍 VID → User Details Fetcher")
st.caption("Advanced user profile view")

# ===============================
# HARDCODED COOKIE (PRIVATE REPO ONLY)
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
    if not ts_val or ts_val == 0:
        return "-"
    return datetime.fromtimestamp(int(ts_val), tz=IST).strftime(
        "%Y-%m-%d %H:%M:%S IST"
    )

def days_ago(ts_val):
    if not ts_val or ts_val == 0:
        return "-"
    now = datetime.now(IST)
    dt = datetime.fromtimestamp(int(ts_val), tz=IST)
    return f"{(now - dt).days} days ago"

def gender(v):
    return {0: "Unknown", 1: "Male", 2: "Female"}.get(v, "Unknown")

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
            # 2️⃣ UID → PROFILE
            # ===============================
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

            info = r2.json()["infos"][0]

            # ===============================
            # PROFILE HEADER (ENHANCED)
            # ===============================
            col1, col2 = st.columns([1, 3])

            with col1:
                st.image(info.get("avatar"), width=200)

            with col2:
                st.markdown(f"## {info.get('nick')}")
                st.code(info.get("uid"), language="text")
                st.caption("UID (click to copy)")

                st.code(info.get("vid"), language="text")
                st.caption("VID (click to copy)")

                st.markdown(f"**Gender:** {gender(info.get('sex'))}")
                st.markdown(f"**Birthday:** {info.get('birthday')}")
                st.markdown(f"**Bio:** {info.get('sign')}")

                st.markdown("### 🕒 Registration")
                st.write(ts_to_ist(info.get("register_time")))
                st.caption(days_ago(info.get("register_time")))

                st.markdown("### 🖼 Avatar URL")
                st.code(info.get("avatar"), language="text")
                st.caption("Tap to copy avatar link")

            st.divider()

        except Exception as e:
            st.error(f"Error occurred: {e}")

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("⚠️ Hardcoded cookie version — keep repository PRIVATE")
