import streamlit as st
import pandas as pd
import time
import Linear_regression
import numpy as np
from datetime import datetime
import requests

API_KEY = "hisAoGNPyeV5DLIXiR5oxfxAO1Q9mYTN"  # Add your Polygon API key here
API_KEY2 = "de64aa57c9f29588cd3a0db5"  # Add your API key here

st.set_page_config(layout="wide")  # Set layout to wide

# Center the title
st.markdown("<h1 style='text-align: center;'>Gordon's FT100 Live Tracker 📈</h1>", unsafe_allow_html=True)

# Progress bar under the title
progress_bar = st.progress(0)

# List of FT100 tickers
ft100_tickers = [
    "AAL.L", "ABF.L", "ADM.L", "AHT.L", "ANTO.L", "AUTO.L", "AV.L", "AVST.L", "AZN.L", "BA.L",
    "BARC.L", "BATS.L", "BDEV.L", "BHP.L", "BP.L", "BRBY.L", "BT-A.L", "CCH.L", "CRH.L", "DCC.L",
    "DGE.L", "EVR.L", "EXPN.L", "FERG.L", "FLTR.L", "FRES.L", "GLEN.L", "GSK.L", "HLMA.L", "HL.L",
    "HSBA.L", "IAG.L", "ICP.L", "IHG.L", "III.L", "IMB.L", "INF.L", "ITRK.L", "JD.L", "JET.L",
    "KGF.L", "LAND.L", "LGEN.L", "LLOY.L", "LSEG.L", "MNDI.L", "MNG.L", "MRO.L", "NG.L", "NXT.L",
    "OCDO.L", "PHNX.L", "POLY.L", "PRU.L", "PSN.L", "PSON.L", "RB.L", "RDSA.L", "RDSB.L", "REL.L",
    "RIO.L", "RMV.L", "RR.L", "RTO.L", "SBRY.L", "SDR.L", "SGE.L", "SGRO.L", "SHP.L", "SKG.L",
    "SLA.L", "SMDS.L", "SMIN.L", "SMT.L", "SN.L", "SPX.L", "SSE.L", "STAN.L", "STJ.L", "SVT.L",
    "TSCO.L", "TW.L", "ULVR.L", "UU.L", "VOD.L", "WPP.L"
]

# Function to get live prices with error handling
def get_live_prices(tickers):
    prices = {}
    for ticker in tickers:
        try:
            url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/2023-01-09/2023-01-09?apiKey={API_KEY}"
            response = requests.get(url)
            data = response.json()
            if 'results' in data:
                prices[ticker] = data['results'][-1]['c']
            else:
                st.error(f"Error fetching live prices for {ticker}: {data.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error fetching live prices for {ticker}: {e}")
    return prices

# Function to get historical data
def get_historical_data(ticker, period="1y"):
    try:
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/2022-01-01/2023-01-01?apiKey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if 'results' in data:
            hist = pd.DataFrame(data['results'])
            hist['Date'] = pd.to_datetime(hist['t'], unit='ms')
            hist.set_index('Date', inplace=True)
            hist.rename(columns={'c': 'Close'}, inplace=True)
            return hist
        else:
            st.error(f"No historical data found for {ticker}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching historical data for {ticker}: {e}")
        return pd.DataFrame()

# Function to predict future prices
def predict_future_prices(data, days=30):
    data = data.reset_index()
    data['Date'] = pd.to_datetime(data['Date'])
    data['Date'] = data['Date'].map(pd.Timestamp.toordinal)
    
    X = np.array(data['Date']).reshape(-1, 1)
    y = np.array(data['Close']).reshape(-1, 1)
    
    model = LinearRegression()
    model.fit(X, y)
    
    future_dates = np.array([data['Date'].max() + i for i in range(1, days + 1)]).reshape(-1, 1)
    future_prices = model.predict(future_dates)
    
    future_data = pd.DataFrame({
        'Date': [pd.Timestamp.fromordinal(int(date)) for date in future_dates],
        'Predicted Close': future_prices.flatten()
    })
    
    return future_data

# Function to get exchange rates
def get_exchange_rates():
    url = f"https://api.exchangerate-api.com/v4/latest/GBP?apikey={API_KEY2}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["rates"]
    else:
        st.error("Error fetching exchange rates")
        return None

# Sidebar for user input
st.sidebar.title("Filter Options")

# Function to trigger rerun
def rerun():
    st.experimental_set_query_params(rerun=str(datetime.now()))

# Initialize session state
if 'selected_ticker' not in st.session_state:
    st.session_state.selected_ticker = ft100_tickers[0]
if 'selected_period' not in st.session_state:
    st.session_state.selected_period = "1y"
if 'selected_currency' not in st.session_state:
    st.session_state.selected_currency = "USD"
if 'amount' not in st.session_state:
    st.session_state.amount = 0.0

selected_ticker = st.sidebar.selectbox("Select a ticker", ft100_tickers, index=ft100_tickers.index(st.session_state.selected_ticker), on_change=rerun)
selected_period = st.sidebar.selectbox("Select period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=["1mo", "3mo", "6mo", "1y", "2y", "5y"].index(st.session_state.selected_period), on_change=rerun)

# Update session state
st.session_state.selected_ticker = selected_ticker
st.session_state.selected_period = selected_period

# Display live prices in the sidebar
st.sidebar.header("Live Prices 💹")
prices = get_live_prices(ft100_tickers)
if prices is not None:
    st.sidebar.write(prices)
refresh_button = st.sidebar.button("Refresh Prices")
if refresh_button:
    prices = get_live_prices(ft100_tickers)
    if prices is not None:
        st.sidebar.write(prices)

# Link to exchange rate converter
st.sidebar.header("Currency Converter 🌍")

# Fetch exchange rates
exchange_rates = get_exchange_rates()
if exchange_rates:
    currencies = list(exchange_rates.keys())
    selected_currency = st.sidebar.selectbox("Select currency", currencies, index=currencies.index(st.session_state.selected_currency), on_change=rerun)
    amount = st.sidebar.number_input("Amount in GBP", min_value=0.0, format="%.2f", value=st.session_state.amount, on_change=rerun)
    
    # Update session state
    st.session_state.selected_currency = selected_currency
    st.session_state.amount = amount
    
    converted_amount = amount * exchange_rates[selected_currency]
    st.sidebar.write(f"{amount} GBP = {converted_amount:.2f} {selected_currency}")

# Create 3 columns with the middle column being very narrow
col1, col2, col3 = st.columns([1, 0.05, 1])

# Display historical data and analytics in the first column
with col1:
    st.header(f"Historical Data and Analytics for {selected_ticker} 📊")
    with st.spinner('Loading historical data...'):
        historical_data = get_historical_data(selected_ticker, selected_period)
        if not historical_data.empty:
            # Historical data graph
            st.line_chart(historical_data['Close'])
            
            # Add a thick line for separation
            st.markdown("<hr style='border: 2px solid black; margin-top: 20px; margin-bottom: 20px;'>", unsafe_allow_html=True)
            
            st.write("Moving Averages")
            historical_data['MA50'] = historical_data['Close'].rolling(window=50).mean()
            historical_data['MA200'] = historical_data['Close'].rolling(window=200).mean()
            
            # Moving averages graph
            st.line_chart(historical_data[['Close', 'MA50', 'MA200']])

# Add a vertical line in the middle column
with col2:
    st.markdown("<div style='border-left: 1px solid black; height: 100%;'></div>", unsafe_allow_html=True)

# Display statistical summary and predicted future prices in the third column
with col3:
    st.header("Summary Statistics 📈")
    
    if not historical_data.empty:
        # Statistical summary table with increased height
        st.write(historical_data.describe(), height=600)
        
        # Add a thick line for separation
        st.markdown("<hr style='border: 2px solid black; margin-top: 20px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        
        st.header("Predicted Future Prices 🔮")
        
        with st.spinner('Predicting future prices...'):
            future_data = predict_future_prices(historical_data)
            
            # Predicted future prices graph
            st.line_chart(future_data.set_index('Date'))

# Update live prices every 60 seconds
st.write("Updating live prices every 60 seconds...")
for i in range(100):
    prices = get_live_prices(ft100_tickers)
    if prices is not None:
        st.write(prices)
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"Last updated: {last_updated} ⏰")
    progress_bar.progress(i + 1)
    time.sleep(0.6)
progress_bar.progress(100)
