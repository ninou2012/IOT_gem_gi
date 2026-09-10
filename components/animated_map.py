import streamlit as st
import pydeck as pdk
import pandas as pd

@st.fragment
def MapComponent():
    st.subheader("🗺️ Suivi Cartographique Thématique")

    if "routes_geometry" not in st.session_state:
        st.session_state.routes_geometry = []
        
    points_data = pd.DataFrame([
        {"lat": 48.8566, "lon": 2.3522, "name": "Dépôt Principal G7", "color": [0, 0, 0]},
        {"lat": 48.8738, "lon": 2.2950, "name": "Zone Étoile (Livraison A)", "color": [255, 165, 0]},
        {"lat": 48.8340, "lon": 2.3800, "name": "Zone Nation (Livraison B)", "color": [255, 165, 0]},
        {"lat": 48.8606, "lon": 2.3376, "name": "Zone Louvre (Livraison C)", "color": [255, 165, 0]},
    ])

    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        data=points_data,
        get_position="[lon, lat]",
        get_color="color",
        get_radius=200,
        pickable=True,
    )

    layers = [scatterplot_layer]
    
    if st.session_state.routes_geometry:
        path_layer = pdk.Layer(
            "PathLayer",
            data=st.session_state.routes_geometry,
            get_path="path",
            get_color="color",          
            get_width="width",          
            width_scale=1,
            width_min_pixels=2,
            pickable=True
        )
        layers.append(path_layer)

    view_state = pdk.ViewState(
        latitude=48.8566,
        longitude=2.3522,
        zoom=11.5,
        pitch=30 
    )

    st.pydeck_chart(pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={"text": "{name} {tooltip_info}"}
    ))
