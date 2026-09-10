import streamlit as st
from services.dvrp_engine import run_optimization

def ControlPanelComponent():
    st.subheader("🎛️ Centre de Contrôle")
    
    def handle_optimize_click():
        status, geometries = run_optimization()
        st.session_state.app_status = status
        st.session_state.routes_geometry = geometries

    def handle_reset_click():
        st.session_state.app_status = "Initialisé"
        st.session_state.routes_geometry = []

    st.button(
        "Calculer les itinéraires réels", 
        on_click=handle_optimize_click, 
        type="primary", 
        use_container_width=True
    )
    st.button(
        "Effacer la carte", 
        on_click=handle_reset_click, 
        use_container_width=True
    )
