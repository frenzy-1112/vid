import streamlit as st
import requests
import json
import time

# ===============================
# STREAMLIT CONFIG
# ===============================
st.set_page_config(
    page_title="VID → User Details Fetcher",
    layout="wide",
)

st.title("🔍 VID → User Details Fetcher")
st.caption("Enter VID and fetch complete user information")

# ===============================
# HARDCODED COOKIE (KEEP REPO PRIVATE)
# ===============================
UAAS_COOKIE = "wEri87yq01Zzqgf4qSTpmddlv6%2FUCMU2DrLW1yOup21B6kswFTe4f1T0syyzDejl%2CnNM9ovMxw68QzWOyQX236BxhgJK9ffj%2BtHd8YDwrmMCxeHcUP3khT7ZIlfNaJH%2FP555SKvk%2BwkLQR%2BxiNEMh6CqdrdI%2F0YkLLRJALxoBMthSdWByXPACYv1L2RehQk8Gc98I9RIG5h11g87OtUXE4Jymwhxz4Y6RdQEcUpSSuOJq3agxtkoAZ2BZrFdG4SwP6AnYaVtghDNjm8G8g9sGSozagbhZxA%2Fde9IDqORxokDpFmCjcQ%2Fcbzg%2F%2Fb4vHfrrUUAyi83RA7l1%2Brq7LBl9Z2yNrbCpDo2adm0Qk57VVRroC5oEv%2BX8RyddWcupr6QTf0bm9KRuE62pKCkfWC37v9ahvIFOrDcO7EfKH33za5cio4SGTBT6LXU4fpMlvbr48NGLvLPCTDWejlROuPZmTQV6vQXnZe6pAGSJePwpMo0v%2FEzV6CN%2Bm4crHWjw091VHKK5f%2BXaxEyfakeEleUZyaYza8BlqCABfbOrWmDV7DeWAi2NTpSBR%2F%2BEmv9AwzLE"

# ===============================
# HELPERS
# ===============================
def ts():
    return str(int(time.time() * 1000))

# ===============================
# INPUT
# ===============================
vid = st.text_input(
    "Enter VID",
    placeholder="177307453",
)

fetch_btn = st.button("🚀 Fetch User Info")

# ===============================
# MAIN LOGIC
# ===============================
if fetch_btn:
    if not vid.isdigit():
        st.error("❌ VID must be numeric")
    else:
        try:
            # ===============================
            # 1️⃣ VID → UID
            # ===============================
            with st.spinner("🔎 Resolving VID → UID..."):
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
                    cookies={
                        "uaasCookie": UAAS_COOKIE
                    },
                    json={
                        "sequence": int(ts()),
                        "vid": int(vid),
                        "t": 1
                    },
                    timeout=20
                )

                resp1 = r1.json()

                if "user_info" not in resp1:
                    st.error("❌ UID not found for this VID")
                    st.stop()

                uid = resp1["user_info"]["uid"]

            st.success(f"✅ UID Found: {uid}")

            # ===============================
            # 2️⃣ UID → USER INFO
            # ===============================
            with st.spinner("📦 Fetching full user details..."):
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

                raw_text = r2.text
                parsed_json = json.loads(raw_text)

            # ===============================
            # OUTPUT
            # ===============================
            st.subheader("📌 Parsed User Data")
            st.json(parsed_json)

            st.subheader("🧾 Raw API Response")
            st.code(raw_text, language="json")

        except Exception as e:
            st.error(f"🔥 Error occurred: {e}")

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("⚠️ Hardcoded cookie version — keep repository PRIVATE")
