# 📈 Stock Market Volatility & Sector Performance Analysis

A data analysis tool exploring volatility, returns and inter-sector correlations across major U.S. stock market sectors using real historical data from Polygon.io.

---

## 🎯 Objective

To systematically analyse how different market sectors behave over time, quantifying:

- **Volatility metrics** — Which sectors carry the highest/lowest risk
- **Risk-adjusted returns** — Sharpe ratios for strategic decision-making
- **Correlation patterns** — How major stocks move relative to each other
- **Diversification insights** — Sector selection for portfolio construction

This project demonstrates quantitative reasoning and analytical skills used in quantitative finance, algorithmic trading, and data-driven investment roles.

---

## 📊 Key Features

- **Multi-sector analysis** — Coverage of 5 major sectors (Technology, Finance, Energy, Healthcare, Consumer)
- **Statistical metrics** — Average daily returns, volatility (std dev) and annualised Sharpe ratios
- **Correlation analysis** — Heatmap visualisation of tech stock interdependencies
- **Professional visualisations** — Publication-ready charts with high DPI output
- **Robust error handling** — Logging and graceful failure modes
- **Object-oriented design** — Modular, extensible codebase

---

## 📈 Outputs

- `sector_volatility.png` — Bar chart comparing volatility across all sectors
- `tech_correlation_heatmap.png` — Correlation matrix heatmap of major tech stocks

---

## ⚙️ Tech Stack

- **Python 3.11+**
- **polygon-api-client** — Enterprise-grade stock market data via Polygon.io
- **pandas** — Data manipulation and time-series analysis
- **numpy** — Numerical computations
- **matplotlib & seaborn** — Professional data visualization

---

## 🚀 Quick Start

1. **Get a free API key from Polygon.io:**
   - Sign up at https://polygon.io (free tier available)
   - Copy your API key from the dashboard

2. **Clone the repository:**
```bash
git clone https://github.com/<your-username>/stock-volatility-analysis.git
cd stock-volatility-analysis
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set your API key:**
```bash
export POLYGON_API_KEY='your_api_key_here'
```
(On Windows: `set POLYGON_API_KEY=your_api_key_here`)

5. **Run the analysis:**
```bash
python3 stock_analysis.py
```

---

## 💡 Example Insights

From a recent analysis run:

- **Technology sector** shows highest volatility (2.24%) — higher risk/reward for active strategies
- **Finance sector** is most stable (1.74%) — suitable for defensive positioning
- **Tech correlations** — MSFT-NVDA (0.628), AAPL-MSFT (0.519), AAPL-NVDA (0.442) show moderate to strong comovement
- **Sharpe ratios** — Finance (1.00) slightly outperforms Technology (0.72) on risk-adjusted basis

---

## 📚 Skills Demonstrated

- **Data Engineering** — API integration, data validation, pipeline orchestration
- **Quantitative Analysis** — Volatility metrics, Sharpe ratios, correlation analysis
- **Software Engineering** — Object-oriented design, error handling, logging, type hints
- **Data Visualisation** — Publication-ready charts, professional formatting
- **Financial Literacy** — Risk/return tradeoffs, diversification, sector dynamics

---

## 🧩 Future Enhancements

- Rolling volatility and beta calculations
- Monte Carlo simulations for portfolio optimization
- Factor analysis (size, value, momentum)
- Interactive Streamlit dashboard for real-time monitoring
- Unit tests and CI/CD pipeline
- Support for cryptocurrency and international markets

---

## 📝 Licence

MIT Licence — feel free to use and modify for personal projects.