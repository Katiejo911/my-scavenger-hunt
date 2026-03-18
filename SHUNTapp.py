import streamlit as st
st.set_page_config(page_title="Hunt", layout="centered")
bg = "#003366"

st.markdown(f"""<style>
    .stApp {{ background-color: {bg}; }}
    h1,h2,h3,p,span,label,.stMarkdown {{ color: white !important; }}
    .stTextInput>div>div>input {{ background-color: white !important; color: black !important; }}
    div.stButton>button {{ background-color: {bg}!important; color: white!important; border: 1px solid #4da6ff!important; border-radius: 10px; width: 100%; }}
    button:has(div:contains("🏴‍☠️")) {{ background-color: transparent!important; border: none!important; color: {bg}!important; box-shadow: none!important; }}
</style>""", unsafe_allow_html=True)

if 'level' not in st.session_state: st.session_state.update({'level':0, 'targets':[], 'page':"Player", 'admin':False})

c1, c2, c3 = st.columns([1,1,1])
with c2:
    if st.button("🏴‍☠️"): st.session_state.page = "Admin" if st.session_state.page == "Player" else "Player"; st.rerun()

if st.session_state.page == "Player":
    st.title("Scavenger Hunt")
    if not st.session_state.targets: st.info("No missions yet. Use the secret spot.")
    elif st.session_state.level < len(st.session_state.targets):
        t = st.session_state.targets[st.session_state.level]
        st.subheader(f"📍 Goal: {t.get('destination','???')}")
        ans = st.text_input("Secret word:", key=f"p_{st.session_state.level}")
        if st.button("Verify"):
            if ans.lower().strip() == t['completion'].lower().strip():
                st.balloons(); st.session_state.level += 1; st.rerun()
            else: st.error("Try again!")
    else: st.header("🏆 Victory!"); st.button("Restart", on_click=lambda: st.session_state.update({'level':0}))
else:
    if not st.session_state.admin:
        if st.text_input("Password:", type="password") == "moravia2026": 
            if st.button("Unlock"): st.session_state.admin = True; st.rerun()
    else:
        st.title("🛠 Admin")
        dest = st.text_input("Destination")
        sol = st.text_input("Answer")
        if st.button("Add") and dest and sol:
            st.session_state.targets.append({"type":"Text", "destination":dest, "completion":sol}); st.rerun()
        if st.button("Clear All"): st.session_state.targets = []; st.rerun()
