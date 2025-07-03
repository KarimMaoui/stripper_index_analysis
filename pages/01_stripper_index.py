# pages/01_stripper_index.py

import streamlit as st
from scripts.stripper_index import compute_stripper_index

st.set_page_config(page_title="Stripper Index Monitor", layout="centered")

st.title("📊 Stripper Index Monitor")
st.markdown("Cet indicateur synthétique reflète le stress économique moyen des puits marginaux aux États-Unis (stripper wells).")

st.markdown("---")

# Sliders interactifs
st.subheader("🔧 Paramètres de simulation")

oil_price = st.slider("Prix WTI (USD)", 30, 100, 75)
transport_cost = st.slider("Coût de transport ($/baril)", 0, 20, 8)
rig_count = st.slider("Nombre de rigs actifs (US)", 200, 800, 520)
differential = st.slider("Spread WTI vs Brent (USD)", -10, 10, -2)
production_cost = st.slider("Coût variable moyen ($/baril)", 10, 60, 40)

# Calcul de l'index
index = compute_stripper_index(oil_price, transport_cost, rig_count, differential, production_cost)

st.markdown("---")

# Affichage résultat
st.metric("📈 Stripper Index", f"{index} / 100")

# Barre colorée indicative
color = "🟩" if index >= 70 else "🟨" if index >= 40 else "🟥"
st.markdown(f"**Niveau de stress sectoriel** : {color} {'Faible' if index >= 70 else 'Modéré' if index >= 40 else 'Élevé'}")

st.caption("ℹ️ L'indicateur est composé de 3 dimensions : marge nette, nombre de rigs, et spread WTI.")
