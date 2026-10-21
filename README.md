# Financial ETL Pipeline

A Python ETL pipeline that extracts historical stock market data from Yahoo Finance, transforms it with Pandas, stores it in SQLite and visualizes it with an interactive Streamlit dashboard. Includes statistical time series analysis (stationarity testing, correlation analysis) and full unit test coverage.

## Motivation

Financial markets generate massive amounts of data every day. This project builds a lightweight ETL pipeline to track and analyze the historical price evolution of the three largest and most recognized tech companies in the world — Apple, Microsoft and Google — and observe how time and seasonality affect their stock market behavior. Microsoft and Google also serve as a proxy to measure the market's reaction to the AI race, while Apple, with no clear AI differential product, provides an interesting contrast.

The pipeline uses SQLite instead of PostgreSQL intentionally: for a project of this scope, a serverless database is the right tool. SQLite requires no infrastructure, runs as a single file and keeps the focus on the ETL logic itself. A production environment with higher data volumes and concurrent access would call for PostgreSQL or a cloud data warehouse.

## Tech Stack
- **Python 3.13**
- **yfinance** — data extraction
- **Pandas** — data transformation
- **SQLite** — data storage
- **Streamlit + Plotly** — interactive dashboard
- **statsmodels** — stationarity testing (Augmented Dickey-Fuller)
- **pytest** — unit testing

## Pipeline Architecture
Yahoo Finance → extract.py → transform.py → load.py → SQLite DB → dashboard.py / analysis.py

## Project Structure

| File | Class | Responsibility |
|------|-------|----------------|
| `extract.py` | `Extractor` | Downloads historical prices from Yahoo Finance via yfinance |
| `transform.py` | `Transformer` | Cleans data, computes % change and 7-day moving average |
| `load.py` | `Loader` | Persists transformed data to SQLite |
| `pipeline.py` | `Pipeline` | Orchestrates the full ETL process |
| `analysis.py` | `StationarityAnalyzer` | ADF stationarity test + correlation analysis |
| `dashboard.py` | — | Interactive Streamlit dashboard with Plotly charts |
| `test_pipeline.py` | — | 6 pytest unit tests covering all pipeline stages |

## How to Run

```bash
pip install -r requirements.txt
python pipeline.py          # runs the full ETL
python analysis.py          # runs stationarity + correlation analysis
python -m streamlit run dashboard.py
pytest test_pipeline.py     # runs all unit tests
```

## Data Analysis

### Closing Prices

Microsoft is the dominant player of the analyzed period. After a drop between May and July, it experienced a sharp surge in August — from $380 to $505 in just two weeks — driven by exceptional quarterly results and the rapid enterprise adoption of Copilot as the AI reference tool, backed by Azure's cloud infrastructure. Google, despite being an early AI player with Gemini, loses momentum from May and fails to replicate Microsoft's August surge, reflecting market skepticism about its competitive position in AI. Apple, without comparable software infrastructure, trades at lower price levels, and notably the iPhone 18 launch had minimal market impact — the annual release cycle no longer generates the surprise effect it once did.

From a statistical perspective, closing prices are **non-stationary** series — neither the mean nor the variance remain constant over time, as the clear upward trend in MSFT demonstrates. This means raw prices cannot be used directly for forecasting with standard time series models. To work with them analytically, the series would need to be differenced, which is precisely what the daily percentage change calculated in this pipeline approximates.

### Daily Percentage Change

This series shows stationarity characteristics — it fluctuates around zero with no clear trend. The MSFT spike in August (+15% in a single day) is the direct reflection of the quarterly earnings release. A move of that magnitude in one day only happens with extraordinary news. A clear correlation between the three companies is also visible — when a macro event occurs (inflation, interest rates, general fear) all three move together regardless of their individual fundamentals. To determine whether the underlying process is AR, MA or ARMA, analyzing the autocorrelation function (ACF) and partial autocorrelation function (PACF) would be required — left as a future improvement.

### 7-Day Moving Average

The moving average removes daily noise and reveals the real trend of each company. Microsoft's vertical jump in August is smoothed out — the +15% single-day spike is diluted across the other 6 days of the week and becomes a progressive rise. The classic **"buy the rumor, sell the news"** pattern is also visible in Apple: the price rises weeks before the iPhone 18 announcement in anticipation of the launch, then drops once confirmed as investors take profits.

## Stationarity Analysis — Augmented Dickey-Fuller Test

The ADF test checks whether a time series has a unit root (non-stationary) or not. A p-value below 0.05 rejects the null hypothesis of a unit root, confirming stationarity.

| Series | p-value | Stationary |
|--------|---------|------------|
| Close_AAPL | > 0.05 | ❌ No |
| pct_change_AAPL | < 0.05 | ✅ Yes |
| Close_MSFT | > 0.05 | ❌ No |
| pct_change_MSFT | < 0.05 | ✅ Yes |
| Close_GOOGL | > 0.05 | ❌ No |
| pct_change_GOOGL | < 0.05 | ✅ Yes |

**Conclusion:** Raw closing prices are non-stationary (trending), while daily percentage changes are stationary. This is the expected behavior for financial time series and confirms that returns, not prices, are the correct input for predictive models.

## Correlation Analysis

### Closing Prices
AAPL and MSFT show a moderate positive correlation (~0.58) — both are large-cap tech stocks exposed to the same macro factors. GOOGL shows a negative correlation with both (~-0.41 with AAPL, ~-0.34 with MSFT) during this period, reflecting its diverging trajectory as it loses ground in the AI race while Microsoft gains.

### Daily % Change
Correlations in daily returns are near zero (0.11, 0.18, 0.01), suggesting that on a day-to-day basis, the three companies move largely independently. The short-term price drivers — earnings, product releases, analyst upgrades — are company-specific, even though the medium-term trends (closing prices) are influenced by shared macro factors.

This distinction is important: **co-movement in price levels does not imply co-movement in daily returns**. For risk management and portfolio construction, returns correlation is the relevant metric.

## Future Improvements

- Calculate ACF and PACF to identify the optimal ARIMA model
- Add volatility analysis (rolling standard deviation)
- Orchestrate the pipeline with Apache Airflow for scheduled execution
- Containerize with Docker for easier deployment