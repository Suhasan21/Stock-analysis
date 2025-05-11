import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(layout="wide", page_title="📊 Stock Market Dashboard", page_icon="📈")

# --- CSS Styling ---
st.markdown("""
<style>
    /* Card Style */
    .stMetric {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: #facc15;
        font-weight: bold;
    }
    /* Section Headers */
    h2 {
        color: #38bdf8;
    }
    /* Background */
    .main {
        background-color: #0f172a;
        color: white;
    }
    /* DataFrames */
    .stDataFrame {
        background-color: #111827;
    }
</style>
""", unsafe_allow_html=True)

# --- Database ---
engine = create_engine("mysql+pymysql://root:suhasan21@localhost:3306/stock")

@st.cache_data
def load_data():
    stock_df = pd.read_sql("SELECT * FROM cleaned_stock", engine)
    volatility_df = pd.read_sql("SELECT * FROM top_10_volatile_stocks", engine)
    cumulative_df = pd.read_sql("SELECT * FROM top_5_cumulative_returns", engine)
    sector_df = pd.read_sql("SELECT * FROM sector_average_yearly_returns", engine)
    correlation_df = pd.read_sql("SELECT * FROM stock_correlation_matrix", engine, index_col="Ticker")
    monthly_df = pd.read_sql("SELECT * FROM top_monthly_gainers_losers", engine)
    return stock_df, volatility_df, cumulative_df, sector_df, correlation_df, monthly_df

# --- Load Data ---
stock_df, volatility_df, cumulative_df, sector_df, correlation_df, monthly_df = load_data()

# --- Summary Calculations ---
stock_df["daily_return"] = stock_df.groupby("Ticker")["close"].pct_change()
yearly_returns = stock_df.groupby("Ticker").apply(
    lambda x: (x.sort_values("date")["close"].iloc[-1] - x.sort_values("date")["close"].iloc[0]) / x.sort_values("date")["close"].iloc[0]
).reset_index(name="Yearly Return")

top_10_green = yearly_returns.sort_values("Yearly Return", ascending=False).head(10)
top_10_loss = yearly_returns.sort_values("Yearly Return").head(10)

last_price = stock_df.groupby("Ticker").last()
num_green = (yearly_returns["Yearly Return"] > 0).sum()
num_red = (yearly_returns["Yearly Return"] < 0).sum()
avg_price = last_price["close"].mean()

# --- Sidebar Branding ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2721/2721297.png", width=100)
st.sidebar.markdown("## 🧭 Navigation")
tab = st.sidebar.radio("Go to Section", [
    "📊 Overview", 
    "📈 Volatility & Return", 
    "📉 Correlation Heatmap", 
    "📅 Monthly Gainers/Losers",
    "📘 Stock Details"  
])

# --- Main Content ---
if tab == "📊 Overview":
    st.title("📊 Market Summary Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("🟩 Green Stocks", num_green)
    col2.metric("🟥 Red Stocks", num_red)
    col3.metric("💰 Avg Price", f"₹{avg_price:.2f}")

    st.markdown("### 🥇 Top 10 Gainers")
    st.dataframe(top_10_green.style.background_gradient(cmap="Greens"))

    st.markdown("### 🛑 Top 10 Losers")
    st.dataframe(top_10_loss.style.background_gradient(cmap="Reds"))

elif tab == "📈 Volatility & Return":
    st.title("📈 Volatility & Cumulative Return")

    # Volatility Chart
    st.markdown("### 🔥 Top 10 Most Volatile Stocks")
    fig1 = px.bar(volatility_df.sort_values("Volatility", ascending=False).head(10),
                  x="Ticker", y="Volatility", color="Volatility", color_continuous_scale="Inferno")
    st.plotly_chart(fig1, use_container_width=True)

    # Cumulative Returns
    st.markdown("### 🚀 Cumulative Returns of Top 5 Performing Stocks")
    cumulative_df["date"] = pd.to_datetime(cumulative_df["date"])
    cum_melted = cumulative_df.melt(id_vars="date", var_name="Ticker", value_name="Cumulative Return")
    fig2 = px.line(cum_melted, x="date", y="Cumulative Return", color="Ticker",
                   color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig2, use_container_width=True)

    # Sector Performance
    st.markdown("### 🏭 Sector-wise Yearly Returns")
    fig3 = px.bar(sector_df, x="Sector", y="Average_Yearly_Return", color="Sector",
                  color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig3, use_container_width=True)

elif tab == "📉 Correlation Heatmap":
    st.title("📉 Stock Price Correlation")
    fig4, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_df.corr(), cmap="coolwarm", annot=False, ax=ax)
    st.pyplot(fig4)

elif tab == "📅 Monthly Gainers/Losers":
    st.title("📅 Monthly Top 5 Gainers and Losers")

    # Clean monthly data
    monthly_df["month_year"] = pd.to_datetime(monthly_df["month_year"]).dt.to_period("M").astype(str)
    monthly_df["type"] = monthly_df["type"].str.strip().str.lower()

    months = monthly_df["month_year"].unique()
    selected_month = st.selectbox("Select Month", sorted(months), index=len(months)-1)
    filtered = monthly_df[monthly_df["month_year"] == selected_month]

    col1, col2 = st.columns(2)
    col1.markdown("#### 📈 Top 5 Gainers")
    gainers = filtered[filtered["type"] == "gainer"].nlargest(5, "pct_return")
    col1.dataframe(gainers.style.background_gradient(cmap="Greens"))

    col2.markdown("#### 📉 Top 5 Losers")
    losers = filtered[filtered["type"] == "loser"].nsmallest(5, "pct_return")
    col2.dataframe(losers.style.background_gradient(cmap="Reds"))


elif tab == "📘 Stock Details":
    st.title("📘 Individual Stock Details")

    tickers = stock_df["Ticker"].unique()
    selected_ticker = st.selectbox("Select a Stock", sorted(tickers))

    stock_data = stock_df[stock_df["Ticker"] == selected_ticker].sort_values("date")
    
    st.markdown(f"### 📈 Price Trend: {selected_ticker}")
    fig = px.line(stock_data, x="date", y="close", title=f"{selected_ticker} Closing Prices", 
                  labels={"close": "Close Price", "date": "Date"})
    st.plotly_chart(fig, use_container_width=True)

    # Daily returns
    stock_data["daily_return"] = stock_data["close"].pct_change()
    avg_return = stock_data["daily_return"].mean()
    volatility = stock_data["daily_return"].std()

    st.markdown("### 📊 Performance Metrics")
    col1, col2 = st.columns(2)
    col1.metric("📈 Average Daily Return", f"{avg_return:.4f}")
    col2.metric("📉 Volatility (Std Dev)", f"{volatility:.4f}")

    # Show data preview
    with st.expander("🔍 View Raw Data"):
        st.dataframe(stock_data[["date", "open", "high", "low", "close", "volume"]].tail(20))
