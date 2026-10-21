import pandas as pd


class Transformer:
    """Handles data transformation and feature engineering."""

    def __init__(self, tickers: list):
        self.tickers = tickers

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans data and adds financial metrics."""

        # Flatten multi-level columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(filter(None, col)).strip('_') for col in df.columns]

        # Keep only relevant columns
        cols = ["Date"] + [f"Close_{t}" for t in self.tickers]
        df = df[cols].copy()

        # Drop rows with missing values
        df.dropna(inplace=True)

        # Add daily percentage change per ticker
        for ticker in self.tickers:
            df[f"pct_change_{ticker}"] = df[f"Close_{ticker}"].pct_change() * 100

        # Add 7-day moving average per ticker
        for ticker in self.tickers:
            df[f"ma7_{ticker}"] = df[f"Close_{ticker}"].rolling(window=7).mean()

        print(f"✅ Transformed {len(df)} records")
        return df


if __name__ == "__main__":
    from extract import Extractor
    tickers = ["AAPL", "MSFT", "GOOGL"]
    raw = Extractor(tickers).extract()
    clean = Transformer(tickers).transform(raw)
    print(clean.head(10))