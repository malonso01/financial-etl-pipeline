import sqlite3
import pandas as pd


class Loader:
    """Handles data loading into SQLite database."""

    def __init__(self, db_path: str = "financial_data.db"):
        self.db_path = db_path

    def load(self, df: pd.DataFrame) -> None:
        """Saves the transformed data to a SQLite database."""
        conn = sqlite3.connect(self.db_path)
        df.to_sql("stock_prices", conn, if_exists="replace", index=False)
        conn.close()
        print(f"✅ Loaded {len(df)} records into '{self.db_path}'")


if __name__ == "__main__":
    from extract import Extractor
    from transform import Transformer

    tickers = ["AAPL", "MSFT", "GOOGL"]
    raw = Extractor(tickers).extract()
    clean = Transformer(tickers).transform(raw)
    Loader().load(clean)