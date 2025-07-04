from scripts import data_loader
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "scripts")))

from scripts import model, visualizer


st.set_page_config(page_title="Stripper Index Simulator", layout="centered")

st.title("🛢️ Stripper Well Profitability Simulator")

st.markdown("### 📈 Données FRED – Marché pétrolier (live)")

col1, col2 = st.columns(2)

with col1:
    wti_price = data_loader.get_latest_value("DCOILWTICO")  # WTI Crude Oil Spot Price
    st.metric("💵 WTI Spot Price", f"{wti_price} USD")

with col2:
    stock_value, prev_week_value, yoy_value = data_loader.get_crude_stock_info()

    if stock_value is None:
        st.metric("📦 Weekly U.S. Ending Crude Stocks", "N/A", help="Impossible de récupérer les données.")
    else:
        variation_week = stock_value - prev_week_value if prev_week_value else None
        variation_yoy = stock_value - yoy_value if yoy_value else None

        label = f"{stock_value:,} kbbl"
        delta_str = f"{variation_week:+,} vs semaine préc." if variation_week else "N/A"
        yoy_str = f"{variation_yoy:+,} vs année préc." if variation_yoy else "N/A"

        st.metric("📦 Weekly U.S. Ending Stocks of Crude Oil", label, delta=delta_str)
        st.caption(f"🔁 Évolution YoY : {yoy_str}")


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



from scripts.stripper_index import compute_stripper_index

index = compute_stripper_index(
    oil_price=75,
    transport_cost=8,
    rig_count=520,
    differential=-2,
    production_cost=40
)

st.metric("📊 Stripper Index", f"{index}/100", help="Indicateur synthétique de rentabilité sectorielle")

