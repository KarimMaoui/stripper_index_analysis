import streamlit as st
from scripts import model, visualizer

st.set_page_config(page_title="Stripper Index Simulator", layout="centered")

st.title("🛢️ Stripper Well Profitability Simulator")

# Inputs interactifs
oil_price = st.slider("Prix du baril (USD)", min_value=20, max_value=100, value=70, step=1)
variable_cost = st.slider("Coût variable de production (USD)", min_value=10, max_value=80, value=40, step=1)

# Résultat
if model.is_profitable(oil_price, variable_cost):
    st.success(f"✅ Rentable à {oil_price} USD/baril (coût = {variable_cost})")
else:
    st.error(f"❌ Pas rentable à {oil_price} USD/baril (coût = {variable_cost})")

st.markdown("---")

# Afficher la matrice complète
st.subheader("📊 Matrice de rentabilité")
price_range = list(range(30, 91, 5))
cost_range = list(range(20, 61, 5))
st.write(dir(visualizer))
visualizer.plot_profitability_matrix(price_range, cost_range)
