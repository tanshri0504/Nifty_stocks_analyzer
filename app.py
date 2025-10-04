import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# Set Streamlit page config
st.set_page_config(page_title="📈 Nifty Stock SMA Viewer", layout="wide")

# App Title
st.title("📊 Nifty Stocks - Interactive SMA Viewer")

# Load and process data
@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found at: {file_path}")

    df = pd.read_csv(file_path)

    # Drop unwanted column
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)

    # Fix data types and clean strings
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Stock'] = df['Stock'].astype(str).str.replace(" ", "", regex=True)

    # Remove rows with invalid dates
    df = df.dropna(subset=['Date'])

    # Sort by date
    df = df.sort_values(by="Date")

    # Calculate SMAs
    df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
    df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()

    return df

# Load the CSV data
csv_path = "Stocks_2025.csv"  # Update if needed
try:
    df = load_data(csv_path)
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# --- Sidebar filters ---
st.sidebar.header("📂 Filters")

# Dropdown: Category
categories = sorted(df['Category'].dropna().unique())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Filter stocks by selected category
filtered_df = df[df['Category'] == selected_category]

# Dropdown: Stock
stocks = sorted(filtered_df['Stock'].dropna().unique())
selected_stock = st.sidebar.selectbox("Select Stock", stocks)

# Filter data for selected stock
stock_data = filtered_df[filtered_df['Stock'] == selected_stock]

# SMA Toggles
show_sma50 = st.sidebar.checkbox("Show SMA 50", value=True)
show_sma200 = st.sidebar.checkbox("Show SMA 200", value=True)

# --- Main chart ---
st.subheader(f"📈 {selected_stock} - Closing Price & SMAs")

if stock_data.empty:
    st.warning("No data available for this stock.")
    st.stop()

# Create interactive Plotly chart
fig = go.Figure()

# Plot Close Price
fig.add_trace(go.Scatter(
    x=stock_data['Date'],
    y=stock_data['Close'],
    mode='lines+markers',
    name='Close Price',
    line=dict(color='green')
))

# Plot SMA 50
if show_sma50:
    fig.add_trace(go.Scatter(
        x=stock_data['Date'],
        y=stock_data['SMA_50'],
        mode='lines',
        name='SMA 50',
        line=dict(color='blue', dash='dash')
    ))

# Plot SMA 200
if show_sma200:
    fig.add_trace(go.Scatter(
        x=stock_data['Date'],
        y=stock_data['SMA_200'],
        mode='lines',
        name='SMA 200',
        line=dict(color='red', dash='dot')
    ))

# Update layout
fig.update_layout(
    title=f"{selected_stock} Price Chart with SMAs",
    xaxis_title="Date",
    yaxis_title="Price",
    xaxis=dict(rangeslider=dict(visible=True)),
    hovermode="x unified",
    template="plotly_white",
    height=600,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Show chart
st.plotly_chart(fig, use_container_width=True)
