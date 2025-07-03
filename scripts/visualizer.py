import plotly.graph_objects as go
import pandas as pd
from scripts import model

def plot_profitability_matrix(price_range, cost_range):
    """
    Affiche une heatmap binaire (rentable ou non) sans échelle continue.
    """
    z_data = []
    for cost in cost_range:
        row = []
        for price in price_range:
            row.append(1 if model.is_profitable(price, cost) else 0)
        z_data.append(row)

    # Création de la heatmap manuelle avec deux couleurs (rouge / vert)
    fig = go.Figure(
        data=go.Heatmap(
            z=z_data,
            x=price_range,
            y=cost_range,
            colorscale=[(0, 'red'), (1, 'green')],
            colorbar=dict(
                tickvals=[0, 1],
                ticktext=['Not Profitable', 'Profitable'],
                title="Profitability"
            ),
            showscale=True
        )
    )

    fig.update_layout(
        title="Stripper Well Profitability Matrix",
        xaxis_title="WTI Price (USD)",
        yaxis_title="Variable Cost (USD)",
        yaxis_autorange="reversed"
    )

    fig.show()

