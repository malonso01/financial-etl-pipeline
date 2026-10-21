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
            # Test closing prices (expected: non-stationary)
            results.append(self.run_adf_test(df[f"Close_{ticker}"], f"Close_{ticker}"))
            # Test daily % change (expected: stationary)
            results.append(self.run_adf_test(df[f"pct_change_{ticker}"], f"pct_change_{ticker}"))

        return pd.DataFrame(results)


if __name__ == "__main__":
    analyzer = StationarityAnalyzer()
    results = analyzer.analyze(["AAPL", "MSFT", "GOOGL"])
    print("\n📋 Summary:")
    print(results[["series", "p_value", "stationary"]].to_string(index=False))