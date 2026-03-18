import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURATION & THEME ---
st.set_page_config(page_title="Scavenger Hunt", layout="centered")

# Custom CSS: Dark Blue Background,  #80bfff Buttons, Invisible Pirate Flag
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #003366;
    }}
    /* Standard Buttons are CYAN */
    div.stButton > button {{
        background-color: #80bfff !important;
        color: black !important;
        border-radius: 10px;
        border: 2px solid #000000;
        font-weight: bold;
    }}
    /* SECRET PIRATE BUTTON: Fully blends with background */
    div.stButton > button:has(div:contains("🏴‍☠️")), 
    div.stButton > button:contains("🏴‍☠️") {{
        background-color: #80bfff !important;
        border: none !important;
        color: #003366 !important;
        box-shadow: none !important;
    }}
    /* Inputs stay white for readability */
    .stTextInput>div>div>input {{
        background-color: white !important;
        color: black !important;
    }}
    /* Force text to be white on the dark blue */
    h1, h2, h3, p, span, label, .stMarkdown {{
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'level' not in st.session_state:
    st.session_state.level = 0
if 'targets' not in st.session_state:
    st.session_state.targets = []
if 'page' not in st.session_state:
    st.session_state.page = "Player"
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False
if 'hint_revealed' not in st.session_state:
    st.session_state.hint_revealed = False

# --- TOP NAVIGATION ICON (The Secret Door) ---
cols = st.columns([1, 1, 1])
with cols[1]:
    if st.button("🏴‍☠️"):
        st.session_state.page = "Admin" if st.session_state.page == "Player" else "Player"
        st.rerun()

# --- PLAYER PAGE ---
if st.session_state.page == "Player":
    st.title("Scavenger Hunt")

    if not st.session_state.targets:
        st.info("No missions have been created yet.")
    elif st.session_state.level < len(st.session_state.targets):
        t = st.session_state.targets[st.session_state.level]
        
        st.subheader("📍 1. Find the Destination")
        if t['type'] == "GPS Coordinates":
            parts = t['destination'].split('|')
            loc_name, lat, lon = parts[0], parts[1], parts[2]
            st.write(f"**Target:** {loc_name}")
            map_url = f"https://maps.google.com/maps?q={lat},{lon}&hl=en&z=17&output=embed"
            st.markdown(f'<iframe width="100%" height="300" src="{map_url}"></iframe>', unsafe_allow_html=True)
        elif t['type'] == "Image URL":
            if t['destination'].startswith("http"):
                st.image(t['destination'], use_column_width=True)
            else:
                st.write(t['destination'])
        
        st.markdown("---")
        st.subheader("🔍 2. Search Clue")
        if not st.session_state.hint_revealed:
            if st.button("💡 Need a hint?"):
                st.session_state.hint_revealed = True
                st.rerun()
        else:
            st.success(f"Hint: {t['orientation']}")

        st.markdown("---")
        ans = st.text_input("Enter secret word:", key=f"p_{st.session_state.level}")
        if st.button("Verify"):
            if ans.lower().strip() == t['completion'].lower().strip():
                st.balloons()
                st.session_state.level += 1
                st.session_state.hint_revealed = False
                st.rerun()
            else:
                st.error("Try again!")
    else:
        st.header("🏆 Victory!")
        if st.button("Restart Hunt"):
            st.session_state.level = 0
            st.session_state.hint_revealed = False
            st.rerun()

# --- ADMIN PAGE ---
else:
    if not st.session_state.admin_authenticated:
        st.title("🔒 Admin Login")
        pw = st.text_input("Enter Admin Password:", type="password")
        if st.button("Unlock"):
            if pw == "moravia2026":
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Wrong password")
    else:
        st.title("🛠 Admin Dashboard")
        if st.button("Log Out"):
            st.session_state.admin_authenticated = False
            st.session_state.page = "Player"
            st.rerun()

        st.subheader("Add New Mission")
        m_type = st.selectbox("Mission Type", ["Text Hint", "GPS Coordinates", "Image URL"])
        
        # DYNAMIC INPUTS BASED ON TYPE
        if m_type == "GPS Coordinates":
            loc_name = st.text_input("Location Name (e.g. Powers Library)")
            lat_val = st.text_input("Latitude")
            lon_val = st.text_input("Longitude")
            dest = f"{loc_name}|{lat_val}|{lon_val}"
        else:
            dest = st.text_input("Destination Name/URL")

        hint = st.text_input("Search Clue (Hint)")
        sol = st.text_input("Completion Word (Answer)")

        if st.button("Add Mission"):
            if dest and hint and sol:
                new_target = {"type": m_type, "destination": dest, "orientation": hint, "completion": sol}
                st.session_state.targets.append(new_target)
                st.success("Mission Added!")
            else:
                st.error("Please fill in all boxes!")
        
        st.markdown("---")
        st.subheader("Current Missions")
        st.write(st.session_state.targets)
        
        if st.button("Clear All Missions"):
            st.session_state.targets = []
            st.rerun()
