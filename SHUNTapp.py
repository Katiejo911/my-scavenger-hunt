import streamlit as st

st.set_page_config(page_title="Scavenger Hunt", layout="centered")

# --- STYLING ---
bg = "#003366"
st.markdown(f"""
<style>
    .stApp {{ background-color: {bg}; }}
    h1, h2, h3, p, span, label, .stMarkdown {{ color: white !important; }}
    .stTextInput>div>div>input {{ background-color: white !important; color: black !important; }}
    
    /* Standard Buttons */
    div.stButton > button {{
        background-color: {bg} !important;
        color: white !important;
        border: 1px solid #4da6ff !important;
        border-radius: 10px;
        width: 100%;
    }}
    /* Ghost Pirate Flag (No Border) */
    button:has(div:contains("🏴‍☠️")) {{
        background-color: transparent !important;
        border: none !important;
        color: {bg} !important;
        box-shadow: none !important;
    }}
    button:has(div:contains("🏴‍☠️")):hover {{ color: white !important; }}
</style>
""", unsafe_allow_html=True)

# --- LOGIC ---
if 'level' not in st.session_state: st.session_state.update({'level':0, 'targets':[], 'page':"Player", 'admin':False})

# Header / Secret Switch
c1, c2, c3 = st.columns([1,1,1])
with c2:
    if st.button("🏴‍☠️"):
        st.session_state.page = "Admin" if st.session_state.page == "Player" else "Player"
        st.rerun()

# --- PLAYER ---
if st.session_state.page == "Player":
    st.title("Scavenger Hunt")
    if not st.session_state.targets:
        st.info("No missions yet. Use the secret spot above.")
    elif st.session_state.level < len(st.session_state.targets):
        t = st.session_state.targets[st.session_state.level]
        st.subheader("📍 1. Find the Destination")
        if t['type'] == "GPS Coordinates":
            loc, lat, lon = t['destination'].split('|')
            st.write(f"**Target:** {loc}")
            map_url = f"https://maps.google.com/maps?q={lat},{lon}&hl=en&z=17&output=embed"
            st.markdown(f'<iframe width="100%" height="300" src="{map_url}"></iframe>', unsafe_allow_html=True)
        else:
            st.write(f"**Go to:** {t['destination']}")
        
        st.markdown("---")
        ans = st.text_input("Enter secret word:", key=f"p_{st.session_state.level}")
        if st.button("Verify"):
            if ans.lower().strip() == t['completion'].lower().strip():
                st.balloons()
                st.session_state.level += 1
                st.rerun()
            else: st.error("Try again!")
    else:
        st.header("🏆 Victory!")
        if st.button("Restart"):
            st.session_state.level = 0
            st.rerun()

# --- ADMIN ---
else:
    if not st.session_state.admin:
        st.title("🔒 Admin Login")
        if st.text_input("Password:", type="password") == "moravia2026":
            if st.button("Unlock"):
                st.session_state.admin = True
                st.rerun()
    else:
        st.title("🛠 Admin Dashboard")
        if st.button("Log Out"):
            st.session_state.admin = False
            st.session_state.page = "Player"
            st.rerun()

        m_type = st.selectbox("Mission Type", ["GPS Coordinates", "Text Hint"])
        if m_type == "GPS Coordinates":
            dest = f"{st.text_input('Name')}|{st.text_input('Lat')}|{st.text_input('Lon')}"
        else:
            dest = st.text_input("Destination")

        hint, sol = st.text_input("Clue"), st.text_input("Answer")
        if st.button("Add Mission") and dest and sol:
            st.session_state.targets.append({"type":m_type, "destination":dest, "orientation":hint, "completion":sol})
            st.rerun()
        
        st.markdown("---")
        if st.button("Clear All"):
            st.session_state.targets = []
            st.rerun()
