# 📊 Stock Market Analysis & Dashboard

A comprehensive stock market analysis and visualization dashboard built with **Streamlit** and **MySQL**, featuring interactive charts, summary statistics, and performance insights across stocks and sectors.

---

## 🚀 Features

- 🟢 Overview of stock market performance
  - Top gainers and losers
  - Count of positive/negative performing stocks
  - Average closing price
  
- 📈 Volatility & Cumulative Return
  - Top 10 most volatile stocks
  - Cumulative returns of top 5 performers
  - Sector-wise yearly return comparison

- 📉 Correlation Analysis
  - Heatmap of correlation between stock prices

- 📅 Monthly Gainers & Losers
  - Monthly breakdown of top 5 gainers and losers

- 📘 Individual Stock Details
  - Interactive price trend visualization
  - Performance metrics (average return, volatility)
  - Raw data preview

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: [MySQL](https://www.mysql.com/) (via SQLAlchemy)
- **Data Handling**: `pandas`, `numpy`
- **Visualization**: `plotly`, `matplotlib`, `seaborn`
- **Dashboard Styling**: HTML/CSS-injected into Streamlit

---

## 📂 Project Structure

```
.
├── stock_app.py                  # Streamlit dashboard app
├── stock.ipynb                   # Jupyter notebook for data preprocessing
├── *.csv                         # Processed data used by the app
├── Stock Analysis.pbix           # Power BI report (optional visualization tool)
└── README.md                     # Project documentation
```

---

## 📦 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/stock-dashboard.git
   cd stock-dashboard
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   If no `requirements.txt`, install manually:
   ```bash
   pip install streamlit pandas matplotlib seaborn plotly sqlalchemy pymysql
   ```

3. **Set Up MySQL Database**

   - Ensure MySQL is installed and running.
   - Create a database named `stock`.
   - Import the required tables (`cleaned_stock`, `top_10_volatile_stocks`, etc.).
   - Update DB credentials in `stock_app.py` if necessary.

4. **Run the App**

   ```bash
   streamlit run stock_app.py
   ```

---

## 📊 Power BI Report

For additional offline or interactive analysis, use the included `Stock Analysis.pbix` Power BI file.

---
