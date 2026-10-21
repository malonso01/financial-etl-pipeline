import pandas as pd

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans data and adds financial metrics."""

    #Flatten multi-level columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(filter(None, col)).strip('_') for col in df.columns]

    #Keep only relevant columns
    df = df[["Date", "Close_AAPL", "Close_MSFT", "Close_GOOGL"]].copy()

    # Drop rows with missing values
    df.dropna(inplace=True)

    #Add daily percentage change per ticker
    for ticker in ["AAPL", "MSFT", "GOOGL"]:
        df[f"pct_change_{ticker}"] = df[f"Close_{ticker}"].pct_change() * 100

    #Add 7-day moving average per ticker
    for ticker in ["AAPL", "MSFT", "GOOGL"]:
        df[f"ma7_{ticker}"] = df[f"Close_{ticker}"].rolling(window=7).mean()

    print(f"✅ Transformed {len(df)} records")
    return df

if __name__ == "__main__":
    from extract import extract
    raw = extract(["AAPL", "MSFT", "GOOGL"])
    clean = transform(raw)
    print(clean.head(10))