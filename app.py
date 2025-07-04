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
    stock_value, prev_value, yoy_value, _ = data_loader.get_crude_stock_info()
    
    if stock_value is None:
        st.metric("📦 Weekly U.S. Ending Stocks of Crude Oil", "N/A")
    else:
        delta_str = "N/A"
        if prev_value:
            delta = ((stock_value - prev_value) / prev_value) * 100
            delta_str = f"{delta:+.2f}% vs semaine préc."

        label = f"{stock_value:,} kbbl"
        st.metric("📦 Weekly U.S. Ending Stocks of Crude Oil", label, delta=delta_str)

        if yoy_value:
            delta_yoy = ((stock_value - yoy_value) / yoy_value) * 100
            st.caption(f"🌀 Évolution YoY : {delta_yoy:+.2f}% vs année préc.")



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



st.markdown("### 🔮 Courbe de Futures WTI")

try:
    futures_curve = data_loader.fetch_wti_futures_curve()

    if futures_curve.isnull().all():
        st.warning("⚠️ Aucune donnée disponible pour les futures WTI.")
    else:
        st.line_chart(futures_curve)
        st.caption("Courbe approximative des contrats à terme sur le WTI (via Yahoo Finance ou fallback manuel si indisponible).")

except Exception as e:
    st.error(f"Erreur lors du chargement de la courbe des futures : {e}")
