import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

def load_data(db_path: str = "financial_data.db") -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM stock_prices", conn)
    conn.close()
    return df

st.title("📈 Financial ETL Dashboard")
st.caption("Data sourced from Yahoo Finance via a Python ETL pipeline")

df = load_data()
df["Date"] = pd.to_datetime(df["Date"])

#Closing prices
st.subheader("Closing Prices")
fig1 = px.line(df, x="Date",
               y=["Close_AAPL", "Close_MSFT", "Close_GOOGL"],
               labels={"value": "Price (USD)", "variable": "Ticker"})
st.plotly_chart(fig1, use_container_width=True)

#Daily % change 
st.subheader("Daily % Change")
fig2 = px.line(df, x="Date",
               y=["pct_change_AAPL", "pct_change_MSFT", "pct_change_GOOGL"],
               labels={"value": "% Change", "variable": "Ticker"})
st.plotly_chart(fig2, use_container_width=True)

#7-day moving average 
st.subheader("7-Day Moving Average")
fig3 = px.line(df, x="Date",
               y=["ma7_AAPL", "ma7_MSFT", "ma7_GOOGL"],
               labels={"value": "Price (USD)", "variable": "Ticker"})
st.plotly_chart(fig3, use_container_width=True)

#Raw data 
with st.expander("View raw data"):
    st.dataframe(df)