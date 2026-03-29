import argparse

import numpy as np
import pandas as pd
import pytest
from unittest.mock import patch

from stock_analysis import SectorAnalyser


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def analyser():
    """SectorAnalyser with a dummy API key; no real network calls are made."""
    with patch("stock_analysis.RESTClient"):
        return SectorAnalyser(api_key="dummy_key", period_days=365, risk_free_rate=0.043)


@pytest.fixture
def price_data():
    """Ten trading days of synthetic closing prices for two tickers."""
    dates = pd.date_range("2024-01-01", periods=10, freq="B")
    return pd.DataFrame(
        {
            "AAPL": [150, 152, 151, 153, 155, 154, 156, 158, 157, 159],
            "MSFT": [300, 303, 301, 305, 308, 307, 310, 312, 311, 314],
        },
        index=dates,
    )


# ---------------------------------------------------------------------------
# calculate_returns()
# ---------------------------------------------------------------------------

class TestCalculateReturns:
    def test_shape_drops_first_row(self, analyser, price_data):
        analyser.price_data = {"Technology": price_data}
        analyser.calculate_returns()
        result = analyser.returns_data["Technology"]
        # pct_change().dropna() removes the first row
        assert result.shape == (9, 2)

    def test_values_are_small_fractions(self, analyser, price_data):
        analyser.price_data = {"Technology": price_data}
        analyser.calculate_returns()
        result = analyser.returns_data["Technology"]
        assert result.abs().max().max() < 0.10

    def test_no_nan_values(self, analyser, price_data):
        analyser.price_data = {"Technology": price_data}
        analyser.calculate_returns()
        assert not analyser.returns_data["Technology"].isnull().any().any()

    def test_empty_dataframe_raises(self, analyser):
        analyser.price_data = {"Technology": pd.DataFrame()}
        with pytest.raises(ValueError):
            analyser.calculate_returns()

    def test_single_price_row_raises(self, analyser):
        single_row = pd.DataFrame(
            {"AAPL": [150]},
            index=pd.date_range("2024-01-01", periods=1),
        )
        analyser.price_data = {"Technology": single_row}
        with pytest.raises(ValueError):
            analyser.calculate_returns()

    def test_multiple_sectors_all_stored(self, analyser, price_data):
        analyser.price_data = {"Technology": price_data, "Finance": price_data.copy()}
        analyser.calculate_returns()
        assert set(analyser.returns_data.keys()) == {"Technology", "Finance"}


# ---------------------------------------------------------------------------
# compute_metrics()
# ---------------------------------------------------------------------------

class TestComputeMetrics:
    def test_columns_present(self, analyser, price_data):
        analyser.price_data = {"Technology": price_data}
        analyser.calculate_returns()
        summary = analyser.compute_metrics()
        for col in ["Avg Daily Return (%)", "Volatility (%)", "Sharpe Ratio (annualised)"]:
            assert col in summary.columns

    def test_sorted_by_volatility_descending(self, analyser):
        dates = pd.date_range("2024-01-01", periods=100, freq="B")
        rng = np.random.default_rng(42)
        analyser.returns_data = {
            "Technology": pd.DataFrame(
                {"A": rng.normal(0.001, 0.02, 100)}, index=dates
            ),
            "Finance": pd.DataFrame(
                {"B": rng.normal(0.001, 0.005, 100)}, index=dates
            ),
        }
        summary = analyser.compute_metrics()
        vols = summary["Volatility (%)"].tolist()
        assert vols == sorted(vols, reverse=True)

    def test_zero_volatility_guard_returns_zero_sharpe(self, analyser):
        dates = pd.date_range("2024-01-01", periods=252, freq="B")
        # np.zeros gives exact 0.0, so std() is exactly 0 and the guard triggers
        returns = pd.DataFrame({"AAPL": np.zeros(252)}, index=dates)
        analyser.returns_data = {"Technology": returns}
        summary = analyser.compute_metrics()
        assert summary.loc["Technology", "Sharpe Ratio (annualised)"] == 0

    def test_sharpe_formula_correctness(self, analyser):
        """Verify the Sharpe calculation matches the expected formula exactly."""
        dates = pd.date_range("2024-01-01", periods=252, freq="B")
        returns_series = np.where(np.arange(252) % 2 == 0, 0.003, -0.001)
        returns = pd.DataFrame({"AAPL": returns_series}, index=dates)
        analyser.returns_data = {"Technology": returns}

        summary = analyser.compute_metrics()

        avg_r = float(np.mean(returns_series))
        vol = float(np.std(returns_series, ddof=1))
        expected = (avg_r * 252 - 0.043) / (vol * np.sqrt(252))
        actual = summary.loc["Technology", "Sharpe Ratio (annualised)"]
        assert abs(actual - expected) < 1e-6

    def test_avg_return_sign(self, analyser):
        dates = pd.date_range("2024-01-01", periods=50, freq="B")
        # All negative daily returns
        returns = pd.DataFrame({"AAPL": [-0.001] * 50}, index=dates)
        analyser.returns_data = {"Technology": returns}
        summary = analyser.compute_metrics()
        assert summary.loc["Technology", "Avg Daily Return (%)"] < 0


# ---------------------------------------------------------------------------
# CLI defaults
# ---------------------------------------------------------------------------

class TestCLIDefaults:
    def _make_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--period", type=int, default=365)
        parser.add_argument("--risk-free-rate", type=float, default=0.043)
        parser.add_argument("--output-dir", type=str, default="output")
        return parser

    def test_period_default(self):
        args = self._make_parser().parse_args([])
        assert args.period == 365

    def test_risk_free_rate_default(self):
        args = self._make_parser().parse_args([])
        assert args.risk_free_rate == 0.043

    def test_output_dir_default(self):
        args = self._make_parser().parse_args([])
        assert args.output_dir == "output"

    def test_custom_period(self):
        args = self._make_parser().parse_args(["--period", "180"])
        assert args.period == 180

    def test_custom_risk_free_rate(self):
        args = self._make_parser().parse_args(["--risk-free-rate", "0.05"])
        assert args.risk_free_rate == 0.05
