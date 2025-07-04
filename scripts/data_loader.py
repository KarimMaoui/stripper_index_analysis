import yfinance as yf
import pandas as pd

def fetch_wti_spot(start="2015-01-01", end=None):
    """
    Télécharge les prix spot du pétrole WTI depuis Yahoo Finance.
    """
    ticker = yf.Ticker("CL=F")  # WTI Crude Oil Futures (front month)
    df = ticker.history(start=start, end=end)
    df = df[['Close']].rename(columns={"Close": "WTI_Spot"})
    df.index = pd.to_datetime(df.index)
    return df

def fetch_wti_futures_curve():
    """
    Récupère une estimation simple de la courbe des futures WTI (approximée).
    ATTENTION : Yahoo Finance ne fournit pas toute la courbe future complète via une seule API.
    Il faut passer par plusieurs tickers mensuels comme CL=F, CLM25.NYM, CLN25.NYM, etc.
    """
    contracts = {
        "M+0": "CL=F",        # Front month
        "M+1": "CLQ25.NYM",   # Exemple : août 2025
        "M+2": "CLU25.NYM",   # septembre 2025
    }

    futures_prices = {}
    for label, ticker in contracts.items():
        try:
            data = yf.Ticker(ticker).history(period="1d")
            price = data["Close"].iloc[-1]
            futures_prices[label] = price
        except:
            futures_prices[label] = None

    return pd.Series(futures_prices, name="WTI_Futures")

if __name__ == "__main__":
    spot_df = fetch_wti_spot()
    print("📈 Prix spot du WTI :")
    print(spot_df.tail())

    futures_curve = fetch_wti_futures_curve()
    print("\n🔮 Courbe futures WTI (approximative) :")
    print(futures_curve)

import pandas as pd
import requests

FRED_API_KEY = "6f5863ca9ddf67a531b77bb50475f173"  # Remplace par ta vraie clé

def fetch_fred_series(series_id, start_date="2025-01-01"):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "observations" not in data:
        print(f"[ERROR] Bad Request. The series '{series_id}' does not exist.")
        return pd.DataFrame(columns=["date", "value"])

    df = pd.DataFrame(data["observations"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    return df.dropna(subset=["value"])[["date", "value"]]

def get_latest_value(series_id):
    df = fetch_fred_series(series_id)
    if df.empty:
        return "N/A"
    return round(df["value"].iloc[-1], 2)



import requests
from bs4 import BeautifulSoup

def get_latest_crude_stock():
    url = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=WCRSTUS1&f=W"
    response = requests.get(url)

    if response.status_code != 200:
        print("[ERROR] Failed to fetch crude stock data")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    try:
        tables = soup.find_all("table")
        for table in tables:
            tds = table.find_all("td")
            # Lire en sens inverse pour trouver la donnée la plus récente
            for td in reversed(tds):
                text = td.get_text(strip=True).replace(",", "")
                if text.isdigit() and len(text) >= 6:
                    return int(text)
        print("[ERROR] No valid stock value found in any table")
        return None
    except Exception as e:
        print(f"[ERROR] Parsing failed: {e}")
        return None


import requests
from bs4 import BeautifulSoup
import datetime

def get_crude_stock_info():
    url = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=WCRSTUS1&f=W"
    response = requests.get(url)
    if response.status_code != 200:
        print("[ERROR] Failed to fetch crude stock data")
        return None, None, None, None

    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")

    stock_values = []

    for table in tables:
        rows = table.find_all("tr")
        if not rows:
            continue
        for row in rows[2:]:  # Skip header
            cells = row.find_all("td")
            if not cells:
                continue
            try:
                year_month = cells[0].get_text(strip=True)
                for i in range(1, len(cells), 2):
                    if i + 1 >= len(cells):
                        break
                    value_str = cells[i + 1].get_text(strip=True).replace(",", "")
                    if value_str.isdigit():
                        value = int(value_str)
                        week_pos = (i + 1) // 2
                        stock_values.append({
                            "month": year_month,
                            "week_pos": week_pos,
                            "value": value
                        })
            except:
                continue

       # Extraire seulement les valeurs (par ordre chronologique)
    numeric_values = [entry["value"] for entry in stock_values]
    if len(numeric_values) < 2:
        return None, None, None, None

    latest_value = numeric_values[-1]
    previous_value = numeric_values[-2]

    # YoY avec week_pos
    latest = stock_values[-1]
    target_month = f"{int(latest['month'].split('-')[0]) - 1}-{latest['month'].split('-')[1]}"
    week_pos = latest["week_pos"]
    yoy_value = None
    for entry in stock_values:
        if entry["month"] == target_month and entry["week_pos"] == week_pos:
            yoy_value = entry["value"]
            break

    return latest_value, previous_value, yoy_value, week_pos
