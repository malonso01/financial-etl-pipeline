# Financial ETL Pipeline

A Python ETL pipeline that extracts historical stock market data from Yahoo Finance, transforms it with Pandas, stores it in SQLite and visualizes it with an interactive Streamlit dashboard.

## Motivation

Financial markets generate massive amounts of data every day. This project builds a lightweight ETL pipeline to track and analyze the historical price evolution of the three largest and most recognized tech companies in the world — Apple, Microsoft and Google — and observe how time and seasonality affect their stock market behavior. Microsoft and Google also serve as a proxy to measure the market's reaction to the AI race, while Apple, with no clear AI differential product, provides an interesting contrast.

The pipeline uses SQLite instead of PostgreSQL intentionally: for a project of this scope, a serverless database is the right tool. SQLite requires no infrastructure, runs as a single file and keeps the focus on the ETL logic itself. A production environment with higher data volumes and concurrent access would call for PostgreSQL or a cloud data warehouse.

## Tech Stack
- **Python 3.13**
- **yfinance** — data extraction
- **Pandas** — data transformation
- **SQLite** — data storage
- **Streamlit + Plotly** — interactive dashboard

## Pipeline Architecture
Yahoo Finance → extract.py → transform.py → load.py → SQLite DB → dashboard.py

## How to Run

```bash
pip install -r requirements.txt
python load.py
python -m streamlit run dashboard.py
```

## Data Analysis

### Closing Prices

Microsoft is the dominant player of the analyzed period. After a drop between May and July, it experienced a sharp surge in August — from $380 to $505 in just two weeks — driven by exceptional quarterly results and the rapid enterprise adoption of Copilot as the AI reference tool, backed by Azure's cloud infrastructure. Google, despite being an early AI player with Gemini, loses momentum from May and fails to replicate Microsoft's August surge, reflecting market skepticism about its competitive position in AI. Apple, without comparable software infrastructure, trades at lower price levels, and notably the iPhone 18 launch had minimal market impact — the annual release cycle no longer generates the surprise effect it once did.

From a statistical perspective, closing prices are **non-stationary** series — neither the mean nor the variance remain constant over time, as the clear upward trend in MSFT demonstrates. This means raw prices cannot be used directly for forecasting with standard time series models. To work with them analytically, the series would need to be differenced, which is precisely what the daily percentage change calculated in this pipeline approximates.

### Daily Percentage Change

This series shows stationarity characteristics — it fluctuates around zero with no clear trend. The MSFT spike in August (+15% in a single day) is the direct reflection of the quarterly earnings release. A move of that magnitude in one day only happens with extraordinary news. A clear correlation between the three companies is also visible — when a macro event occurs (inflation, interest rates, general fear) all three move together regardless of their individual fundamentals. To determine whether the underlying process is AR, MA or ARMA, analyzing the autocorrelation function (ACF) and partial autocorrelation function (PACF) would be required — left as a future improvement.

### 7-Day Moving Average

The moving average removes daily noise and reveals the real trend of each company. Microsoft's vertical jump in August is smoothed out — the +15% single-day spike is diluted across the other 6 days of the week and becomes a progressive rise. The classic **"buy the rumor, sell the news"** pattern is also visible in Apple: the price rises weeks before the iPhone 18 announcement in anticipation of the launch, then drops once confirmed as investors take profits.

## Future Improvements

- Add Dickey-Fuller test to automatically validate stationarity
- Calculate ACF and PACF to identify the optimal ARIMA model
- Orchestrate the pipeline with Apache Airflow for scheduled execution
- Containerize with Docker for easier deployment
- Add unit tests with pytest