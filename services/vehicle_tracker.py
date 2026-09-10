import streamlit as st

def init_state():
    if "app_status" not in st.session_state:
        st.session_state.app_status = "Initialisé - Prêt"
    if "vehicles_data" not in st.session_state:
        st.session_state.vehicles_data = {
            "Camion_A": {"lat": 48.8566, "lon": 2.3522},
            "Camion_B": {"lat": 48.8738, "lon": 2.2950}
        }
