import streamlit as st
import time
import pandas as pd
from services.vehicle_tracker import get_latest_positions

@st.fragment(run_every=2.0)
def MapComponent():
    """
    Composant autonome (Fragment). 
    S'actualise toutes les 2 secondes sans impacter le reste de l'UI.
    """
    st.subheader("🗺️ Cartographie de la Flotte")
    
    # Récupération des données rafraîchies via notre service
    positions = get_latest_positions()
    
    # Affichage d'un indicateur visuel de rafraîchissement local
    st.caption(f"⚡ Synchronisation IoT locale : {time.strftime('%H:%M:%S')}")
    
    if positions:
        # Transformation des données pour le composant carte natif de Streamlit
        df = pd.DataFrame([
            {"lat": v["lat"], "lon": v["lon"], "name": k} 
            for k, v in positions.items()
        ])
        
        # Rendu de la carte (Remplace le rendu lourd d'un re-run global)
        st.map(df, zoom=11)
    else:
        st.info("En attente de réception des premières coordonnées GPS...")
