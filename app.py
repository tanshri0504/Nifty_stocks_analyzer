import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Set page configuration
st.set_page_config(page_title="Nifty Stock SMA Viewer", layout="wide")
st.title("📈 Nifty Stocks - SMA Viewer")

# Load and process data with caching
@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found at: {file_path}")

    df = pd.read_csv(file_path)

    # Clean up
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)

    # Fix types and spacing
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Stock'] = df['Stock'].astype(str).str.replace(" ", "", regex=True)

    # Handle possible NaT in dates
    df = df.dropna(subset=['Date'])

    # Add SMA columns
    df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
    df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()

    return df

# Path to your CSV file
csv_path = "Stocks_2025.csv"  # Make sure this is the correct relative path

try:
    df = load_data(csv_path)
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# Sidebar - Filters
st.sidebar.header("🔍 Filter Options")

categories = sorted(df['Category'].dropna().unique())
selected_category = st.sidebar.selectbox("Select Category", categories)

filtered_df = df[df['Category'] == selected_category]

stocks = sorted(filtered_df['Stock'].dropna().unique())
selected_stock = st.sidebar.selectbox("Select Stock", stocks)

stock_data = filtered_df[filtered_df['Stock'] == selected_stock]

if stock_data.empty:
    st.warning("No data available for this stock.")
    st.stop()

# Chart
st.subheader(f"📊 Price and Moving Averages for: *{selected_stock}*")

fig, ax = plt.subplots(figsize=(14, 6))

sns.lineplot(data=stock_data, x="Date", y="Close", label="Close", color='green', marker='D')
sns.lineplot(data=stock_data, x="Date", y="SMA_50", label="SMA 50", color='blue')
sns.lineplot(data=stock_data, x="Date", y="SMA_200", label="SMA 200", color='red')

ax.set_title(f"{selected_stock} - Closing Price with SMA 50 & SMA 200", fontsize=16)
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()
plt.xticks(rotation=45)

st.pyplot(fig)
