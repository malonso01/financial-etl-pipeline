import yfinance as yf
import pandas as pd


class Extractor:
    """Handles data extraction from Yahoo Finance."""

    def __init__(self, tickers: list, period: str = "6mo"):
        self.tickers = tickers
        self.period = period

    def extract(self) -> pd.DataFrame:
        """Downloads historical stock prices from Yahoo Finance."""
        df = yf.download(self.tickers, period=self.period, progress=False, auto_adjust=True)
        df.reset_index(inplace=True)
        print(f"✅ Extracted {len(df)} records for {self.tickers}")
        return df


if __name__ == "__main__":
    extractor = Extractor(tickers=["AAPL", "MSFT", "GOOGL"])
    df = extractor.extract()
    print(df.head())