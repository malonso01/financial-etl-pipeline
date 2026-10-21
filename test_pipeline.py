import pytest
import pandas as pd
from extract import Extractor
from transform import Transformer
from load import Loader


# --- Extractor tests ---
def test_extractor_returns_dataframe():
    extractor = Extractor(["AAPL"], period="1mo")
    df = extractor.extract()
    assert isinstance(df, pd.DataFrame)

def test_extractor_not_empty():
    extractor = Extractor(["AAPL"], period="1mo")
    df = extractor.extract()
    assert len(df) > 0


# --- Transformer tests ---
def test_transformer_returns_dataframe():
    tickers = ["AAPL", "MSFT", "GOOGL"]
    raw = Extractor(tickers, period="1mo").extract()
    clean = Transformer(tickers).transform(raw)
    assert isinstance(clean, pd.DataFrame)

def test_transformer_has_expected_columns():
    tickers = ["AAPL", "MSFT", "GOOGL"]
    raw = Extractor(tickers, period="1mo").extract()
    clean = Transformer(tickers).transform(raw)
    for ticker in tickers:
        assert f"Close_{ticker}" in clean.columns
        assert f"pct_change_{ticker}" in clean.columns
        assert f"ma7_{ticker}" in clean.columns

def test_transformer_no_nulls_in_close():
    tickers = ["AAPL", "MSFT", "GOOGL"]
    raw = Extractor(tickers, period="1mo").extract()
    clean = Transformer(tickers).transform(raw)
    for ticker in tickers:
        assert clean[f"Close_{ticker}"].isnull().sum() == 0


# --- Loader tests ---
def test_loader_creates_db(tmp_path):
    tickers = ["AAPL", "MSFT", "GOOGL"]
    raw = Extractor(tickers, period="1mo").extract()
    clean = Transformer(tickers).transform(raw)
    db_path = tmp_path / "test.db"
    Loader(str(db_path)).load(clean)
    assert db_path.exists()
    