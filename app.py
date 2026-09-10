import streamlit as st
from services.vehicle_tracker import init_state
from components.animated_map import MapComponent
from components.control_panel import ControlPanelComponent

st.set_page_config(
    page_title="G7 IoT DVRP Monitor",
    layout="wide",
    initial_sidebar_state="expanded"
)

def App():
    st.title("🚀 G7 IoT DVRP - Tableau de bord Temps Réel")
    st.caption("Architecture réactive inspirée de React JS — Sans st.rerun()")
    st.markdown("---")

    init_state()

    col_map, col_ctrl = st.columns([2, 1], gap="medium")

    with col_map:
        MapComponent()
        st.markdown("""
        **Légende des Itinéraires :**  
        🔴 Ligne Épaisse Rouge : Tournée **Critique** (Poids Lourd)  
        🔵 Ligne Fine Bleue : Tournée **Normale** (Véhicule Léger)
        """)

    with col_ctrl:
        ControlPanelComponent()
        
        st.markdown("---")
        st.markdown("### 📊 Métriques Globales")
        st.metric(
            label="Statut du Système", 
            value=st.session_state.app_status
        )
        st.metric(
            label="Nombre de Véhicules Actifs", 
            value=len(st.session_state.vehicles_data)
        )

if __name__ == "__main__":
    App()
