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

