import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURATION & THEME ---
st.set_page_config(page_title="Scavenger Hunt", layout="centered")

# Custom CSS: Background is DARK BLUE, Buttons are CYAN
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #003366;
    }}
    /* Standard Buttons are CYAN */
    div.stButton > button {{
        background-color: #00FFFF !important;
        color: black !important;
        border-radius: 10px;
        border: 2px solid #000000;
        font-weight: bold;
    }}
    /* SECRET PIRATE BUTTON: Matches background color exactly to hide it */
    div.stButton > button:has(div:contains("🏴‍☠️")), 
    div.stButton > button:contains("🏴‍☠️") {{
        background-color: #003366 !important;
        border: none !important;
        color: #003366 !important; /* Makes the icon itself blend in too until hovered */
        box-shadow: none !important;
    }}
    .stTextInput>div>div>input {{
        background-color: white;
    }}
    /* White text for visibility on dark blue */
    h1, h2, h3, p, span, label {{
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

# --- TOP NAVIGATION ICON ---
cols = st.columns([1, 1, 1])
with cols[1]:
    # This is the "Invisible" button
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
            st.info(f"Target: {loc_name}")
            map_url = f"https://maps.google.com/maps?q={lat},{lon}&hl=en&z=17&output=embed"
            st.markdown(f'<iframe width="100%" height="300" src="{map_url}"></iframe>', unsafe_allow_html=True)
        elif t['type'] == "Image URL":
            if t['destination'].startswith("http"):
                st.image(t['destination'], use_column_width=True)
            else:
                st.info(t['destination'])
        
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
            st.session
