import streamlit as st
from services.vehicle_tracker import init_state
from components.animated_map import MapComponent
from components.control_panel import ControlPanelComponent

# Configuration de la page Streamlit
st.set_page_config(
    page_title="G7 IoT DVRP Monitor",
    layout="wide",
    initial_sidebar_state="expanded"
)

def App():
    """
    Composant Racine de l'application (Équivalent de <App /> en React).
    Gère le layout général et l'injection de l'état global.
    """
    st.title("🚀 G7 IoT DVRP - Tableau de bord Temps Réel")
    st.caption("Architecture réactive inspirée de React JS — Sans st.rerun()")
    st.markdown("---")

    # Hook d'initialisation de l'état (Équivalent de useState / Context)
    init_state()

    # Layout en colonnes (Layout Grid)
    col_map, col_ctrl = st.columns(2, gap="medium")

    with col_map:
        # Rendu du composant cartographique autonome
        MapComponent()

    with col_ctrl:
        # Rendu du panneau de configuration et d'actions
        ControlPanelComponent()
        
        # Section d'affichage des KPI globaux abonnés à l'état
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
