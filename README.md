# Stock Market Volatility & Sector Performance Analysis

A data analysis tool exploring volatility, returns and inter-sector correlations across major U.S. stock market sectors using real historical data from Polygon.io.

---

## Objective

To systematically analyse how different market sectors behave over time, quantifying:

- **Volatility metrics** - which sectors carry the highest/lowest risk
- **Risk-adjusted returns** - Sharpe ratios for strategic decision-making
- **Correlation patterns** - how major stocks move relative to each other
- **Diversification insights** - sector selection for portfolio construction

This project demonstrates quantitative reasoning and analytical skills relevant to quantitative finance, algorithmic trading, and data-driven investment roles.

---

## Key Features

- **Multi-sector analysis** - covers 5 major sectors (Technology, Finance, Energy, Healthcare, Consumer)
- **Statistical metrics** - average daily returns, volatility (std dev) and annualised Sharpe ratios
- **Correlation analysis** - heatmap visualisation of tech stock interdependencies
- **Rolling volatility** - 30-day rolling annualised volatility chart showing risk through time
- **CSV export** - sector metrics table saved alongside charts for further analysis
- **CLI arguments** - configurable period, risk-free rate, and output directory
- **Professional visualisations** - publication-ready charts at 300 DPI
- **Robust error handling** - logging and graceful failure modes
- **Object-oriented design** - modular, extensible codebase
- **Unit tested** - 16 tests covering core calculations with no real API calls required

---

## Outputs

| File | Description |
|---|---|
| `sector_volatility.png` | Bar chart comparing volatility across all sectors |
| `tech_correlation_heatmap.png` | Correlation matrix heatmap of major tech stocks |
| `rolling_volatility.png` | 30-day rolling annualised volatility by sector |
| `sector_metrics.csv` | Sector summary: Sharpe ratio, avg return, volatility |

---

## Tech Stack

- **Python 3.11+**
- **polygon-api-client** - real-time and historical stock market data via Polygon.io
- **pandas** - data manipulation and time-series analysis
- **numpy** - numerical computations
- **matplotlib & seaborn** - data visualisation
- **pytest** - unit testing

---

## Quick Start

1. **Get a free API key from Polygon.io:**
   - Sign up at https://polygon.io (free tier available)
   - Copy your API key from the dashboard

2. **Clone the repository:**
```bash
git clone https://github.com/aravinth-kanesh/stock-volatility-analysis.git
cd stock-volatility-analysis
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set your API key** (choose one method):

   **Option A - .env file (recommended):**
   ```bash
   cp .env.example .env
   # Open .env and paste your Polygon.io key
   ```

   **Option B - environment variable:**
   ```bash
   export POLYGON_API_KEY='your_api_key_here'
   # On Windows: set POLYGON_API_KEY=your_api_key_here
   ```

5. **Run the analysis:**
```bash
python3 stock_analysis.py
```

---

## CLI Arguments

| Argument | Default | Description |
|---|---|---|
| `--period` | `365` | Days of historical data to fetch |
| `--risk-free-rate` | `0.043` | Annualised risk-free rate for Sharpe calculation |
| `--output-dir` | `output/` | Directory to save charts and CSV |

**Examples:**
```bash
# Default settings (1 year of data)
python3 stock_analysis.py

# 6 months of data, save outputs to a subdirectory
python3 stock_analysis.py --period 180 --output-dir ./results

# Override the risk-free rate
python3 stock_analysis.py --risk-free-rate 0.05
```

---

## Running Tests

No API key is required - all tests use injected synthetic data.

```bash
pip install pytest
pytest tests/ -v
```

---

## Project Structure

```
stock-volatility-analysis/
├── stock_analysis.py          # Main application
├── requirements.txt           # Runtime dependencies
├── .env.example               # API key template
├── tests/
│   └── test_sector_analyser.py
└── .github/
    └── workflows/
        └── ci.yml             # GitHub Actions CI
```

---

## Example Insights

From a recent analysis run:

- Technology shows the highest volatility (2.24%) - higher risk/reward for active strategies
- Finance is the most stable sector (1.74%) - suitable for defensive positioning
- Tech correlations: MSFT-NVDA (0.628), AAPL-MSFT (0.519), AAPL-NVDA (0.442)
- On a risk-adjusted basis, Finance (Sharpe 1.00) slightly outperforms Technology (0.72)
