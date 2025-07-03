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



from bs4 import BeautifulSoup

def get_latest_crude_stock():
    """
    Scrape le dernier chiffre de stock de brut aux US depuis l’EIA.
    Retourne la dernière valeur en milliers de barils (int) ou None si échec.
    """
    url = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=WCRSTUS1&f=W"

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Cherche la première table contenant les données (ignore les tables de légende)
        tables = soup.find_all("table")
        target_table = None
        for table in tables:
            if table.find("th") and "Weekly U.S. Ending Stocks of Crude Oil" in table.text:
                target_table = table
                break
        if not target_table:
            print("[ERROR] No valid table found.")
            return None

        # Trouve la dernière ligne contenant une valeur numérique
        rows = target_table.find_all("tr")
        for row in reversed(rows):
            cols = row.find_all("td")
            if len(cols) >= 2:
                value_str = cols[1].text.strip().replace(",", "")
                try:
                    return int(float(value_str))
                except ValueError:
                    continue

    except Exception as e:
        print("[ERROR] Failed to fetch crude stock data:", e)

    return None
