import plotly.graph_objects as go
import pandas as pd
from scripts import model
import streamlit as st



def plot_profitability_matrix(price_range, cost_range):
    """
    Heatmap avec échelle de profit multi-niveaux (7 couleurs) centrée sur 0.
    """
    z_data = []
    for cost in cost_range:
        row = []
        for price in price_range:
            margin = price - cost
            row.append(margin)
        z_data.append(row)

    fig = go.Figure(
        data=go.Heatmap(
            z=z_data,
            x=price_range,
            y=cost_range,
            colorscale=[
                [0.0, 'darkred'],
                [0.2, 'red'],
                [0.35, 'yellow'],
                [0.5, 'lightgreen'],
                [0.65, 'green'],
                [0.8, 'darkgreen'],
                [1.0, 'darkgreen']
            ],
            zmin=-30,
            zmax=70,
            colorbar=dict(
                title="Profit Margin ($/barrel)",
                titleside='right'
            )
        )
    )

    fig.update_layout(
        title="Profit Margin Matrix (Price - Cost)",
        xaxis_title="WTI Price (USD)",
        yaxis_title="Variable Cost (USD)",
        yaxis_autorange="reversed"
    )

    st.plotly_chart(fig)

