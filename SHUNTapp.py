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
