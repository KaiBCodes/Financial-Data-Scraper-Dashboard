import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# User input for stock ticker
st.write("## Stock Data Dashboard")
ticker = st.text_input("Enter a stock ticker symbol (e.g., AAPL, MSFT, TSLA):", "AAPL")

# Fetch stock data
stock_data = yf.Ticker(ticker)
history = stock_data.history(period="1y")

# Ensure history dates are timezone-naive
history.index = history.index.tz_localize(None)

# Select start and end dates
st.write("### Select Date Range")
start_date = st.date_input("Start date", value=pd.to_datetime("2023-01-01"))
end_date = st.date_input("End date", value=pd.to_datetime("2023-12-31"))

# Convert start_date and end_date to timezone-naive
start_date = pd.to_datetime(start_date).tz_localize(None)
end_date = pd.to_datetime(end_date).tz_localize(None)

# Filter the data based on the selected date range
if start_date > end_date:
    st.error("Error: End date must fall after start date.")
else:
    filtered_data = history.loc[start_date:end_date]
    st.write(f"### {ticker} Stock Data from {start_date} to {end_date}")
    st.dataframe(filtered_data)

    # Plot closing price
    st.write("### Closing Price Over Time")
    plt.figure(figsize=(10, 4))
    plt.plot(filtered_data.index, filtered_data['Close'], label='Close Price')
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"{ticker} Closing Price")
    plt.grid(True)
    st.pyplot(plt)

    # Plot trading volume
    st.write("### Trading Volume Over Time")
    plt.figure(figsize=(10, 4))
    plt.bar(filtered_data.index, filtered_data['Volume'], color='orange', label='Volume')
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.title(f"{ticker} Trading Volume")
    plt.grid(True)
    st.pyplot(plt)

    # Calculate and plot moving averages
    st.write("### Moving Averages (20-day and 50-day)")
    filtered_data['MA20'] = filtered_data['Close'].rolling(window=20).mean()
    filtered_data['MA50'] = filtered_data['Close'].rolling(window=50).mean()

    plt.figure(figsize=(10, 4))
    plt.plot(filtered_data.index, filtered_data['Close'], label='Close Price')
    plt.plot(filtered_data.index, filtered_data['MA20'], label='20-Day MA')
    plt.plot(filtered_data.index, filtered_data['MA50'], label='50-Day MA')
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"{ticker} Moving Averages")
    plt.grid(True)
    plt.legend()
    st.pyplot(plt)
