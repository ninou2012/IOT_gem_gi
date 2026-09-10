import streamlit as st
from services.dvrp_engine import run_optimization

def ControlPanelComponent():
    """
    Composant d'action (UI Statique émettant des événements).
    Utilise les mécanismes de callbacks de Streamlit (on_click / on_change).
    """
    st.subheader("🎛️ Centre de Commande")
    
    # Définition des Event Handlers (Style React : handleAction)
    def handle_optimize_click():
        st.session_state.app_status = "⚡ Calcul d'optimisation..."
        # Appel de la logique métier
        resultat = run_optimization()
        st.session_state.app_status = resultat

    def handle_reset_click():
        st.session_state.app_status = "Initialisé"
        st.session_state.vehicles_data = {}

    # Rendu des éléments d'interface
    st.write("Interactions sur l'algorithme DVRP :")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button(
            "Optimiser les Routes", 
            on_click=handle_optimize_click, 
            type="primary", 
            use_container_width=True
        )
    with col2:
        st.button(
            "Réinitialiser", 
            on_click=handle_reset_click, 
            type="secondary", 
            use_container_width=True
        )
