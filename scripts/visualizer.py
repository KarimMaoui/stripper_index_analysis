import plotly.express as px
import pandas as pd
from scripts import model

def plot_profitability_matrix(price_range, cost_range):
    """
    Affiche une heatmap interactive de rentabilité selon les coûts et prix du baril.
    """
    data = []
    results = model.simulate_profitability_thresholds(price_range, cost_range)

    for cost in cost_range:
        for i, price in enumerate(price_range):
            data.append({
                "Cost": cost,
                "Price": price,
                "Profitable": "Yes" if results[cost][i] else "No"
            })

    df = pd.DataFrame(data)

    fig = px.imshow(
        df.pivot(index="Cost", columns="Price", values="Profitable") == "Yes",
        labels=dict(x="WTI Price (USD)", y="Variable Cost (USD)", color="Profitable"),
        color_continuous_scale=["red", "green"],
        aspect="auto",
        title="Stripper Well Profitability Matrix"
    )
    fig.update_layout(xaxis_title="WTI Price", yaxis_title="Variable Cost")
    fig.show()

