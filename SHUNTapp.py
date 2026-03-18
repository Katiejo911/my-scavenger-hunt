import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURATION & THEME ---
st.set_page_config(page_title="Scavenger Hunt", layout="centered")

# THE COLOR PALETTE
bg_color = "#003366"  # Dark Blue
btn_color = "#80bfff" # Light Blue

# Custom CSS
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
    }}
    
    /* 1. Reset ALL buttons to Light Blue #80bfff first */
    div.stButton > button {{
        background-color: {btn_color} !important;
        color: black !important;
        border-radius: 10px;
        border: 2px solid #000000;
        font-weight: bold;
        width: 100%;
    }}

    /* 2. THE STEALTH FIX: Force the first button (the flag) to be GHOSTED */
    /* We target the specific container for the flag button */
    [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button {{
        background-color: transparent !important;
        border: none !important;
        color: {bg_color} !important;
        box-shadow: none !important;
    }}
    
    /* Only show the flag when you hover over the secret spot */
    [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button:hover {{
        color: white !important;
    }}

    /* Text & Input styling */
    h1, h2, h3, p, span, label, .stMarkdown {{
        color: white !important;
    }}
    .stTextInput>div>div>input {{
        background-color: white !important;
        color: black !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
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

# --- TOP NAVIGATION (The Secret Door) ---
# We use three columns to put the "Invisible" button in the center
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🏴‍☠️"):
        st.session_state.page = "Admin" if st.session_state.page == "Player" else "Player"
        st.rerun()

# --- PLAYER PAGE ---
if st.session_state.page == "Player":
    st.title("Scavenger Hunt")

    if not st.session_state.targets:
        st.info("No missions yet. Find the secret spot at the top to log in.")
    elif st.session_state.level < len(st.session_state.targets):
        t = st.session_state.targets[st.session_state.level]
        st.subheader("📍 1. Find the Destination")
        
        if t['type'] == "GPS Coordinates":
            parts = t['destination'].split('|')
            loc_name, lat, lon = parts[0], parts[1], parts[2]
            st.write(f"**Target:** {loc_name}")
            map_url = f"https://maps.google.com/maps?q={lat},{lon}&hl=en&z=17&output=embed"
            st.markdown(f'<iframe width="100%" height="300" src="{map_url}"></iframe>', unsafe_allow_html=True)
        else:
            st.write(f"**Go to:** {t['destination']}")
        
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
        # GPS is now the first/default choice
        m_type = st.selectbox("Mission Type", ["GPS Coordinates", "Text Hint", "Image URL"])
        
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
                st.session_state.targets.append({"type": m_type, "destination": dest, "orientation": hint, "completion": sol})
                st.success("Mission Added!")
                st.rerun()
            else:
                st.error("Fill in all boxes!")
        
        st.markdown("---")
        st.subheader("Current Missions")
        st.write(st.session_state.targets)
        if st.button("Clear All Missions"):
            st.session_state.targets = []
            st.rerun()
