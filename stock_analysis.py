import argparse
import logging
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from polygon import RESTClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SectorAnalyser:
    """Analyse stock sector performance, volatility, and correlations using Polygon.io."""

    def __init__(self, api_key: str, period_days: int = 365, risk_free_rate: float = 0.043):
        """
        Initialise the analyser with Polygon.io API key.

        Args:
            api_key: Your Polygon.io API key
            period_days: Number of days of historical data to fetch (default 365 = 1 year)
            risk_free_rate: Annualised risk-free rate for Sharpe ratio calculation (default 0.043)
        """
        self.client = RESTClient(api_key=api_key)
        self.period_days = period_days
        self.risk_free_rate = risk_free_rate
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=period_days)

        self.stocks = {
            "Technology": ["AAPL", "MSFT", "NVDA"],
            "Finance": ["JPM", "BAC", "GS"],
            "Energy": ["XOM", "CVX", "COP"],
            "Healthcare": ["JNJ", "PFE", "UNH"],
            "Consumer": ["PG", "KO", "WMT"]
        }
        self.price_data = {}
        self.returns_data = {}

    def fetch_data(self) -> None:
        """Fetch historical price data for all sectors using Polygon.io."""
        try:
            logger.info(f"Fetching {self.period_days} days of data from Polygon.io...")

            for sector, tickers in self.stocks.items():
                sector_data = {}

                for ticker in tickers:
                    try:
                        logger.info(f"Fetching {ticker}...")
                        aggs = []

                        # Fetch data in chunks (Polygon API has limits)
                        for agg in self.client.list_aggs(
                                ticker=ticker,
                                multiplier=1,
                                timespan="day",
                                from_=self.start_date.strftime("%Y-%m-%d"),
                                to=self.end_date.strftime("%Y-%m-%d"),
                                limit=50000
                        ):
                            aggs.append(agg)

                        if not aggs:
                            logger.warning(f"⚠️  No data retrieved for {ticker}")
                            continue

                        # Convert to DataFrame
                        data_list = [{
                            "timestamp": agg.timestamp,
                            "close": agg.close
                        } for agg in aggs]

                        df = pd.DataFrame(data_list)
                        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
                        df.set_index("timestamp", inplace=True)
                        df.sort_index(inplace=True)

                        sector_data[ticker] = df["close"]
                        logger.info(f"✅ {ticker} downloaded: {len(df)} records")

                    except Exception as e:
                        logger.warning(f"⚠️  Failed to fetch {ticker}: {e}")
                        continue

                if sector_data:
                    self.price_data[sector] = pd.DataFrame(sector_data)
                    logger.info(f"✅ {sector} sector complete: {len(sector_data)} tickers\n")
                else:
                    logger.warning(f"⚠️  No data retrieved for {sector} sector")

            if not self.price_data:
                raise ValueError("No data retrieved for any sector. Check your API key and internet connection.")

            logger.info(f"✅ Data fetched for {len(self.price_data)} sectors!\n")

        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            raise

    def calculate_returns(self) -> None:
        """Calculate daily percentage returns for each sector."""
        try:
            for sector, df in self.price_data.items():
                if df.empty or len(df) < 2:
                    logger.warning(f"⚠️  Insufficient data for {sector}, skipping")
                    continue

                returns_df = df.pct_change().dropna()

                if returns_df.empty:
                    logger.warning(f"⚠️  No returns calculated for {sector}")
                    continue

                self.returns_data[sector] = returns_df

            if not self.returns_data:
                raise ValueError("No returns data available.")

            logger.info("✅ Returns calculated successfully!\n")

        except Exception as e:
            logger.error(f"Error calculating returns: {e}")
            raise

    def compute_metrics(self) -> pd.DataFrame:
        """Compute volatility and average returns by sector."""
        metrics = []

        for sector, returns_df in self.returns_data.items():
            avg_return = returns_df.mean().mean()
            volatility = returns_df.std().mean()
            sharpe_ratio = (avg_return * 252 - self.risk_free_rate) / (volatility * np.sqrt(252)) if volatility > 0 else 0

            metrics.append({
                "Sector": sector,
                "Avg Daily Return (%)": avg_return * 100,
                "Volatility (%)": volatility * 100,
                "Sharpe Ratio (annualised)": sharpe_ratio
            })

        summary = pd.DataFrame(metrics).set_index("Sector").sort_values("Volatility (%)", ascending=False)
        logger.info(f"📊 Sector Summary:\n{summary}\n")
        return summary

    def plot_volatility(self, summary: pd.DataFrame, output_dir: str = ".") -> None:
        """Plot sector volatility comparison."""
        try:
            output_file = os.path.join(output_dir, "sector_volatility.png")
            fig, ax = plt.subplots(figsize=(10, 6))
            summary["Volatility (%)"].plot(kind="bar", ax=ax, color="coral", edgecolor="black")
            ax.set_title("Sector Volatility Comparison (1Y)", fontsize=14, fontweight="bold")
            ax.set_ylabel("Volatility (% Std Dev of Returns)", fontsize=12)
            ax.set_xlabel("Sector", fontsize=12)
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(output_file, dpi=300)
            plt.close()
            logger.info(f"✅ Volatility chart saved as '{output_file}'")
        except Exception as e:
            logger.error(f"Error plotting volatility: {e}")

    def plot_correlation_heatmap(self, output_dir: str = ".") -> None:
        """Plot correlation heatmap for technology stocks."""
        try:
            if "Technology" not in self.returns_data:
                logger.warning("⚠️  Technology sector data not available for correlation analysis")
                return

            output_file = os.path.join(output_dir, "tech_correlation_heatmap.png")
            tech_returns = self.returns_data["Technology"]
            corr_matrix = tech_returns.corr()

            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr_matrix, annot=True, fmt=".3f", cmap="coolwarm", center=0,
                        cbar_kws={"label": "Correlation"}, ax=ax, square=True, linewidths=0.5)
            ax.set_title("Tech Stocks Correlation Matrix (1Y)", fontsize=14, fontweight="bold")
            plt.tight_layout()
            plt.savefig(output_file, dpi=300)
            plt.close()
            logger.info(f"✅ Correlation heatmap saved as '{output_file}'")
            logger.info(f"\n💡 Tech Stocks Correlation:\n{corr_matrix}\n")
        except Exception as e:
            logger.error(f"Error plotting correlation: {e}")

    def generate_insights(self, summary: pd.DataFrame) -> None:
        """Generate and log key insights."""
        top_sector = summary["Volatility (%)"].idxmax()
        bottom_sector = summary["Volatility (%)"].idxmin()
        top_return = summary["Avg Daily Return (%)"].idxmax()

        logger.info("🔍 Key Insights:")
        logger.info(
            f"  • {top_sector} shows highest volatility ({summary.loc[top_sector, 'Volatility (%)']:.2f}%) — higher risk/reward for active strategies")
        logger.info(
            f"  • {bottom_sector} is most stable ({summary.loc[bottom_sector, 'Volatility (%)']:.2f}%) — suitable for defensive positioning")
        logger.info(
            f"  • {top_return} generated highest avg daily returns ({summary.loc[top_return, 'Avg Daily Return (%)']:.3f}%)")
        logger.info(f"  • Tech sector shows strong correlations — consider diversification within sector")
        logger.info("✅ Analysis complete!\n")

    def run(self, output_dir: str = ".") -> pd.DataFrame:
        """Execute full analysis pipeline."""
        self.fetch_data()
        self.calculate_returns()
        summary = self.compute_metrics()
        self.plot_volatility(summary, output_dir=output_dir)
        self.plot_correlation_heatmap(output_dir=output_dir)
        self.generate_insights(summary)
        return summary

if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description="Stock sector volatility analysis using Polygon.io.")
    parser.add_argument("--period", type=int, default=365,
                        help="Days of historical data to fetch (default: 365)")
    parser.add_argument("--risk-free-rate", type=float, default=0.043,
                        help="Annualised risk-free rate for Sharpe ratio calculation (default: 0.043)")
    parser.add_argument("--output-dir", type=str, default=".",
                        help="Directory to save output charts and CSV (default: current directory)")
    args = parser.parse_args()

    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        logger.error("POLYGON_API_KEY not set. Create a .env file (see .env.example) or export the variable.")
        exit(1)

    analyser = SectorAnalyser(api_key=api_key, period_days=args.period, risk_free_rate=args.risk_free_rate)
    analyser.run(output_dir=args.output_dir)