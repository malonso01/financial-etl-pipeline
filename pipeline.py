from extract import Extractor
from transform import Transformer
from load import Loader


class Pipeline:
    """Orchestrates the full ETL process."""

    def __init__(self, tickers: list, period: str = "6mo", db_path: str = "financial_data.db"):
        self.tickers = tickers
        self.extractor = Extractor(tickers, period)
        self.transformer = Transformer(tickers)
        self.loader = Loader(db_path)

    def run(self):
        """Runs the full ETL pipeline."""
        print("🚀 Starting ETL pipeline...")
        raw = self.extractor.extract()
        clean = self.transformer.transform(raw)
        self.loader.load(clean)
        print("✅ Pipeline completed successfully.")


if __name__ == "__main__":
    pipeline = Pipeline(tickers=["AAPL", "MSFT", "GOOGL"])
    pipeline.run()