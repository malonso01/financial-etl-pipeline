import sqlite3
import pandas as pd
from statsmodels.tsa.stattools import adfuller


class StationarityAnalyzer:
    """Tests stationarity of financial time series using the Augmented Dickey-Fuller test."""

    def __init__(self, db_path: str = "financial_data.db"):
        self.db_path = db_path

    def load_data(self) -> pd.DataFrame:
        """Loads data from SQLite database."""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql("SELECT * FROM stock_prices", conn)
        conn.close()
        return df

    def run_adf_test(self, series: pd.Series, name: str) -> dict:
        """Runs Augmented Dickey-Fuller test on a single series."""
        result = adfuller(series.dropna())
        p_value = result[1]
        is_stationary = p_value < 0.05

        print(f"\n📊 {name}")
        print(f"   ADF Statistic : {result[0]:.4f}")
        print(f"   p-value       : {p_value:.4f}")
        print(f"   Stationary    : {'✅ Yes' if is_stationary else '❌ No'} (p < 0.05)")

        return {"series": name, "adf_stat": result[0], "p_value": p_value, "stationary": is_stationary}

    def analyze(self, tickers: list) -> pd.DataFrame:
        """Runs ADF test on closing prices and daily % change for each ticker."""
        df = self.load_data()
        results = []

        print("=" * 50)
        print("STATIONARITY ANALYSIS — Augmented Dickey-Fuller")
        print("=" * 50)

        for ticker in tickers:
            results.append(self.run_adf_test(df[f"Close_{ticker}"], f"Close_{ticker}"))
            results.append(self.run_adf_test(df[f"pct_change_{ticker}"], f"pct_change_{ticker}"))

        return pd.DataFrame(results)

    def correlation_analysis(self, tickers: list) -> pd.DataFrame:
        """Analyzes correlation between ticker closing prices and daily returns."""
        df = self.load_data()
        
        close_cols = [f"Close_{t}" for t in tickers]
        corr_close = df[close_cols].corr()

        pct_cols = [f"pct_change_{t}" for t in tickers]
        corr_pct = df[pct_cols].corr()

        print("\n" + "=" * 50)
        print("CORRELATION ANALYSIS — Closing Prices")
        print("=" * 50)
        print(corr_close.to_string())

        print("\n" + "=" * 50)
        print("CORRELATION ANALYSIS — Daily % Change")
        print("=" * 50)
        print(corr_pct.to_string())

        return corr_pct


if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL"]
    analyzer = StationarityAnalyzer()

    results = analyzer.analyze(tickers)
    print("\n📋 Summary:")
    print(results[["series", "p_value", "stationary"]].to_string(index=False))

    analyzer.correlation_analysis(tickers)
