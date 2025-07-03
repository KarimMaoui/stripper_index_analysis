# stripper_index_analysis

# Stripper Index Analysis

This project explores the dynamics of the Stripper Well Index — a proxy for low-volume oil production in the United States — in relation to crude oil prices, marginal production costs, and supply elasticity. 

## 📌 Objective

To build a robust Python framework for collecting, cleaning, modeling, and visualizing data around stripper well activity and its economic thresholds.

## 🔍 Key Features

- API-based data import (EIA, Yahoo Finance, Baker Hughes)
- Time-series analysis of the Stripper Index vs WTI
- Profitability thresholds based on cost structures
- Visual dashboard (Plotly or Streamlit)
- Forward-looking scenario modeling

## 📊 Data Sources

- [U.S. Energy Information Administration (EIA)](https://www.eia.gov/)
- [Baker Hughes Rig Count](https://bakerhughesrigcount.gcs-web.com/)
- [WTI Futures & Spot Prices](https://finance.yahoo.com/quote/CL%3DF/)
- [Texas Railroad Commission](https://www.rrc.texas.gov/)

## 🧠 Use Cases

- Estimate shut-in price thresholds for stripper wells
- Backtest oil supply reactivity based on historical price cycles
- Assess long-term investment signals from marginal production

## ⚙️ Tech Stack

- Python 3.10+
- pandas, numpy, yfinance, requests
- matplotlib, plotly, seaborn
- Streamlit (for web dashboard)
- Jupyter notebooks

## 📁 Project Structure

```bash
stripper_index_analysis/
├── data/                # Raw and processed data
├── notebooks/           # Jupyter exploration & modeling
├── stripper_index/      # Python modules (data, viz, models)
├── reports/             # Final figures and written summaries
├── requirements.txt     # Dependencies
└── README.md            # This file
