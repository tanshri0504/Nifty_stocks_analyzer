import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(page_title="Nifty Stock Viewer", layout="wide")
st.title("📈 Nifty Stocks SMA Visualizer")

# Load and preprocess the data
@st.cache_data
def load_data():
    df = pd.read_csv("Stocks_2025.csv")
    df = df.drop('Unnamed: 0', axis=1)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Stock'] = df['Stock'].str.replace(" ", "", regex=True)
    df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
    df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Stocks")
categories = df['Category'].unique()
selected_category = st.sidebar.selectbox("Select Category", sorted(categories))

filtered_df = df[df['Category'] == selected_category]
stocks = filtered_df['Stock'].unique()
selected_stock = st.sidebar.selectbox("Select Stock", sorted(stocks))

stock_df = filtered_df[filtered_df['Stock'] == selected_stock]

# Plotting
st.subheader(f"📊 Stock Price and SMAs for **{selected_stock}**")

fig, ax = plt.subplots(figsize=(14,6))

sns.lineplot(data=stock_df, x="Date", y="Close", label="Close", color='green', marker='D')
sns.lineplot(data=stock_df, x="Date", y="SMA_50", label="SMA 50", color='blue')
sns.lineplot(data=stock_df, x="Date", y="SMA_200", label="SMA 200", color='red')

ax.set_title(f"{selected_stock} Price with SMA 50 & SMA 200", fontsize=16)
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.xticks(rotation=45)
plt.legend()
st.pyplot(fig)
