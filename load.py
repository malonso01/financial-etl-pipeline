import sqlite3
import pandas as pd

def load(df: pd.DataFrame, db_path: str = "financial_data.db") -> None:
    """Saves the transformed data to a SQLite database."""

    conn = sqlite3.connect(db_path)
    df.to_sql("stock_prices", conn, if_exists="replace", index=False)
    conn.close()

    print(f"✅ Loaded {len(df)} records into '{db_path}'")


if __name__ == "__main__":
    from extract import extract
    from transform import transform

    raw = extract(["AAPL", "MSFT", "GOOGL"])
    clean = transform(raw)
    load(clean)