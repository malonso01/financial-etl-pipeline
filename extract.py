import yfinance as yf
import pandas as pd

def extract(tickers: list, period: str = "6mo") -> pd.DataFrame:
    """Downloads historical stock prices from Yahoo Finance."""
    df = yf.download(tickers, period=period, progress=False, auto_adjust=True)
    df.reset_index(inplace=True)
    print(f"✅ Extracted {len(df)} records for {tickers}")
    return df

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL"]
    df = extract(tickers)
    print(df.head())