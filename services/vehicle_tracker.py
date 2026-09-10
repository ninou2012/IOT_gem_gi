import streamlit as st
import random

def init_state():
    """Initialise le dictionnaire d'état (useState)."""
    if "app_status" not in st.session_state:
        st.session_state.app_status = "Initialisé"
    if "vehicles_data" not in st.session_state:
        st.session_state.vehicles_data = {
            "Camion_A": {"lat": 48.8566, "lon": 2.3522},
            "Camion_B": {"lat": 48.8738, "lon": 2.2950}
        }

def get_latest_positions():
    """
    Lit ou génère de nouvelles données. 
    En production, cette fonction lirait le buffer de mqtt_manager.py
    """
    # On simule un léger mouvement des véhicules pour voir la carte bouger
    for vehicle in st.session_state.vehicles_data:
        if "lat" in st.session_state.vehicles_data[vehicle]:
            st.session_state.vehicles_data[vehicle]["lat"] += random.uniform(-0.002, 0.002)
            st.session_state.vehicles_data[vehicle]["lon"] += random.uniform(-0.002, 0.002)
        
    return st.session_state.vehicles_data
