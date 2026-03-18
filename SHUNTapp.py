import streamlit as st

# MUST BE THE FIRST ST LINE: Sets the browser tab and phone home-screen icon
st.set_page_config(page_title="Scavenger Hunt", page_icon="🏴‍☠️")

# 1. Styling - Blue Background (#0077be), Cyan Buttons (#0FD3FA)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0077be; }} 
    
    /* Global lettering is White */
    h1, h2, h3, p, span, label, .stMarkdown {{ 
        color: white !important; 
        text-align: center; 
    }}
    
    /* Standard Buttons (Cyan) */
    div.stButton > button {{ 
        background-color: #0FD3FA; 
        color: black; 
        border-radius: 10px; 
        font-weight: bold; 
        width: 100%; 
        border: none !important;
    }}
    
    /* THE SECRET DOOR: Invisible override for the top button */
    div[data-testid="column"]:nth-of-type(2) button {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: white !important;
        font-size: 24px !important;
    }}
    div[data-testid="column"]:nth-of-type(2) button:hover,
    div[data-testid="column"]:nth-of-type(2) button:active,
    div[data-testid="column"]:nth-of-type(2) button:focus {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    /* Input Box Styling */
    input, textarea {{ background-color: white !important; color: black !important; }}
    </style>
    """, unsafe_allow_html=True)

# 2. Initialize Data (Session State)
if 'targets' not in st.session_state: st.session_state.targets = []
if 'level' not in st.session_state: st.session_state.level = 0
if 'page' not in st.session_state: st.session_state.page = "Player"
if 'hint_revealed' not in st.session_state: st.session_state.hint_revealed = False
if 'admin_authenticated' not in st.session_state: st.session_state.admin_authenticated = False

# --- SECRET TOP BUTTON (The Gateway) ---
col_l, col_m, col_r = st.columns([1,1,1])
with col_m:
    if st.button("🏴‍☠️", key="secret_gate"):
        st.session_state.page = "Admin"
        st.rerun()

# --- PLAYER VIEW ---
if st.session_state.page == "Player":
    st.title("Scavenger Hunt")
    
    if not st.session_state.targets:
        st.warning("No missions have been created yet.")
    elif st.session_state.level < len(st.session_state.targets):
        t = st.session_state.targets[st.session_state.level]
        
        # Mission Navigation
        head_col, back_col = st.columns([3, 1])
        head_col.header(f"Mission {st.session_state.level + 1}")
        
        if st.session_state.level > 0:
            if back_col.button("🔙 BACK"):
                st.session_state.level -= 1
                st.session_state.hint_revealed = False
                st.rerun()
        
        # 1. Destination
        st.subheader("📍 1. Find the Destination")
        if t['type'] == "GPS Coordinates":
            parts = t['destination'].split('|')
            loc_name, lat, lon = parts[0], parts[1], parts[2]
            st.info(f"Target: {loc_name}")
            map_html = f'<iframe width="100%" height="300" frameborder="0" src="https://maps.google.com/maps?q={lat},{lon}&hl=en&z=17&output=embed"></iframe>'
            st.components.v1.html(map_html, height=310)
        elif t['type'] == "Image URL":
            if t['destination'].startswith("http"): st.image(t['destination'], use_column_width=True)
        else:
            st.info(t['destination'])
        
        # 2. Hint
        st.markdown("---")
        st.subheader("🔍 2. Search Clue")
        if not st.session_state.hint_revealed:
            if st.button("💡 Need a hint?"):
                st.session_state.hint_revealed = True
                st.rerun()
        else:
            st.success(f"Hint: {t['orientation']}")
        
        # 3. Entry
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
            dest = st.text_input("Destination (or Name|Lat|Lon)")
            hint = st.text_input("Search Clue (Hint)")
            sol = st.text_input("Completion Word (Answer)")

            if st.button("Add Mission"):
                new_target = {"type": m_type, "destination": dest, "orientation": hint, "completion": sol}
                st.session_state.targets.append(new_target)
                st.success("Mission Added!")
                
            st.markdown("---")
            st.subheader("Current Missions")
            st.write(st.session_state.targets)
            
            if st.button("Clear All Missions"):
                st.session_state.targets = []
                st.rerun()
