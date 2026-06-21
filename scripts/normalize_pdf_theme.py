from __future__ import annotations

import io
from pathlib import Path
from textwrap import wrap

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
PDF_ROOT = ROOT / "manuals" / "pdf"

NAVY = colors.HexColor("#10203A")
NAVY_2 = colors.HexColor("#152B4C")
INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#647086")
BLUE = colors.HexColor("#2C74B8")
GOLD = colors.HexColor("#C89B3C")
PAPER = colors.HexColor("#F7F9FC")
LINE = colors.HexColor("#D8DEE8")


MANUALS = {
    "lotq-0001-exponents-logarithms-compounding-for-quant-research-manual.pdf": {
        "id": "LOTQ-0001",
        "title": "Exponents, Logarithms, and Compounding",
        "category": "Core Math",
        "difficulty": "Beginner",
        "subtitle": "Growth, decay, returns, logs, and compounding for quant research systems.",
    },
    "lotq-0002-quant-arithmetic-ratios-log-returns-manual.pdf": {
        "id": "LOTQ-0002",
        "title": "Arithmetic, Ratios, and Log Returns",
        "category": "Core Math",
        "difficulty": "Beginner",
        "subtitle": "Convert prices into ratios, returns, cumulative paths, and research-ready series.",
    },
    "lotq-0003-quant-calculus-foundations-market-models-manual.pdf": {
        "id": "LOTQ-0003",
        "title": "Calculus Foundations for Market Models",
        "category": "Calculus",
        "difficulty": "Beginner",
        "subtitle": "Derivatives, integrals, optimization, sensitivity, and continuous-growth intuition.",
    },
    "lotq-0004-quant-derivatives-rates-sensitivity-manual.pdf": {
        "id": "LOTQ-0004",
        "title": "Derivatives, Rates of Change, and Sensitivity",
        "category": "Calculus",
        "difficulty": "Intermediate",
        "subtitle": "Local change, gradients, Greeks, marginal risk, and robustness diagnostics.",
    },
    "lotq-0005-functions-graphs-transformations-field-guide.pdf": {
        "id": "LOTQ-0005",
        "title": "Functions, Graphs, and Transformations",
        "category": "Functions",
        "difficulty": "Beginner",
        "subtitle": "Function behavior, graph transformations, feature maps, and quant pipeline intuition.",
    },
    "lotq-0006-quant-sequences-series-financial-growth-manual.pdf": {
        "id": "LOTQ-0006",
        "title": "Sequences, Series, and Financial Growth",
        "category": "Core Math",
        "difficulty": "Beginner",
        "subtitle": "Ordered values, summed values, compounding, discounting, and equity-curve mechanics.",
    },
    "lotq-0007-quant-integrals-accumulation-expected-value-manual.pdf": {
        "id": "LOTQ-0007",
        "title": "Integrals, Accumulation, and Expected Value",
        "category": "Calculus",
        "difficulty": "Intermediate",
        "subtitle": "Accumulation, discounting, scenario weighting, expected value, and numeric methods.",
    },
    "lotq-0008-functions-expanded-field-guide-intermediate.pdf": {
        "id": "LOTQ-0008",
        "title": "Functions Expanded Field Guide",
        "category": "Functions",
        "difficulty": "Intermediate",
        "subtitle": "Function families, formulas, graph behavior, research uses, and common traps.",
    },
    "lotq-0009-algebra-foundations-for-quant-research-manual.pdf": {
        "id": "LOTQ-0009",
        "title": "Algebra Foundations for Quant Research",
        "category": "Algebra",
        "difficulty": "Beginner",
        "subtitle": "Variables, equations, constraints, scaling, PnL formulas, and formula debugging.",
    },
    "lotq-0010-quant-linear-algebra-foundations-for-quant-research-manual.pdf": {
        "id": "LOTQ-0010",
        "title": "Linear Algebra Foundations for Quant Research",
        "category": "Linear Algebra",
        "difficulty": "Beginner",
        "subtitle": "Vectors, matrices, covariance, regression geometry, PCA, and implementation hazards.",
    },
    "lotq-0011-quant-vectors-matrices-factor-models-manual.pdf": {
        "id": "LOTQ-0011",
        "title": "Vectors, Matrices, and Factor Models",
        "category": "Linear Algebra",
        "difficulty": "Intermediate",
        "subtitle": "Exposure vectors, return matrices, factor models, risk decompositions, and attribution.",
    },
    "lotq-0012-autocorrelation-and-mean-reversion.pdf": {
        "id": "LOTQ-0012",
        "title": "Autocorrelation and Mean Reversion",
        "category": "Time Series",
        "difficulty": "Intermediate",
        "subtitle": "Serial dependence, mean reversion evidence, decay, validation, and regime-break controls.",
    },
    "lotq-0013-conditional-probability-and-bayes-rule.pdf": {
        "id": "LOTQ-0013",
        "title": "Conditional Probability and Bayes' Rule",
        "category": "Probability",
        "difficulty": "Intermediate",
        "subtitle": "Conditional questions, denominator audits, Bayesian updates, forecasts, and uncertainty controls.",
    },
    "lotq-0014-confidence-intervals-and-error-bounds.pdf": {
        "id": "LOTQ-0014",
        "title": "Confidence Intervals and Error Bounds",
        "category": "Statistics",
        "difficulty": "Intermediate",
        "subtitle": "Uncertainty ranges, error bounds, dependent returns, tail risk, and monitored estimates.",
    },
    "lotq-0015-constrained-optimization-and-portfolio-weights.pdf": {
        "id": "LOTQ-0015",
        "title": "Constrained Optimization and Portfolio Weights",
        "category": "Optimization",
        "difficulty": "Advanced",
        "subtitle": "Portfolio constraints, objectives, active limits, executable weights, and allocation diagnostics.",
    },
    "lotq-0016-correlation-covariance-and-dependence.pdf": {
        "id": "LOTQ-0016",
        "title": "Correlation, Covariance, and Dependence",
        "category": "Probability",
        "difficulty": "Intermediate",
        "subtitle": "Joint movement, covariance, stable dependence, nonlinear tails, and matrix workflows.",
    },
    "lotq-0017-descriptive-statistics-for-market-data.pdf": {
        "id": "LOTQ-0017",
        "title": "Descriptive Statistics for Market Data",
        "category": "Statistics",
        "difficulty": "Beginner",
        "subtitle": "Market-data summaries, distribution shape, timing, weighting, and production metrics.",
    },
    "lotq-0018-eigenvalues-pca-dimensionality-reduction.pdf": {
        "id": "LOTQ-0018",
        "title": "Eigenvalues, PCA, and Dimensionality Reduction",
        "category": "Linear Algebra",
        "difficulty": "Intermediate",
        "subtitle": "Covariance geometry, components, dimensionality reduction, and leakage-safe PCA workflows.",
    },
    "lotq-0019-expectation-variance-skewness-and-kurtosis.pdf": {
        "id": "LOTQ-0019",
        "title": "Expectation, Variance, Skewness, and Kurtosis",
        "category": "Probability",
        "difficulty": "Beginner",
        "subtitle": "Distribution moments, payoff shape, portfolio risk, instability, and point-in-time statistics.",
    },
    "lotq-0020-hypothesis-testing-and-statistical-significance.pdf": {
        "id": "LOTQ-0020",
        "title": "Hypothesis Testing and Statistical Significance",
        "category": "Statistics",
        "difficulty": "Intermediate",
        "subtitle": "Defensible tests, uncertainty, false discoveries, effect sizes, and research decisions.",
    },
    "lotq-0021-multiple-regression-and-feature-interpretation.pdf": {
        "id": "LOTQ-0021",
        "title": "Multiple Regression and Feature Interpretation",
        "category": "Statistics",
        "difficulty": "Intermediate",
        "subtitle": "Regression specifications, conditional effects, attribution, incremental information, and validation.",
    },
    "lotq-0022-optimization-foundations-for-quant-research.pdf": {
        "id": "LOTQ-0022",
        "title": "Optimization Foundations for Quant Research",
        "category": "Optimization",
        "difficulty": "Intermediate",
        "subtitle": "Objectives, convexity, optimality, algorithms, numerical failures, and decision validation.",
    },
    "lotq-0023-overfitting-noise-and-statistical-illusions.pdf": {
        "id": "LOTQ-0023",
        "title": "Overfitting, Noise, and Statistical Illusions",
        "category": "Research Methodology",
        "difficulty": "Intermediate",
        "subtitle": "False discovery, search risk, time-series validation, apparent alpha, and research governance.",
    },
    "lotq-0024-probability-foundations-for-quant-research.pdf": {
        "id": "LOTQ-0024",
        "title": "Probability Foundations for Quant Research",
        "category": "Probability",
        "difficulty": "Beginner",
        "subtitle": "Events, distributions, probability updates, finite-data estimates, and probabilistic decisions.",
    },
    "lotq-0025-random-variables-and-distributions.pdf": {
        "id": "LOTQ-0025",
        "title": "Random Variables and Distributions",
        "category": "Probability",
        "difficulty": "Beginner",
        "subtitle": "Numerical uncertainty, distributions, model families, simulation, and system contracts.",
    },
    "lotq-0026-regression-foundations-for-quant-research.pdf": {
        "id": "LOTQ-0026",
        "title": "Regression Foundations for Quant Research",
        "category": "Statistics",
        "difficulty": "Intermediate",
        "subtitle": "Regression questions, linear models, assumptions, uncertainty, and leakage-safe systems.",
    },
    "lotq-0027-sampling-estimation-and-uncertainty.pdf": {
        "id": "LOTQ-0027",
        "title": "Sampling, Estimation, and Uncertainty",
        "category": "Statistics",
        "difficulty": "Beginner",
        "subtitle": "Valid samples, estimators, finite-data uncertainty, market dependence, and decision controls.",
    },
    "lotq-0028-stationarity-trends-and-regime-changes.pdf": {
        "id": "LOTQ-0028",
        "title": "Stationarity, Trends, and Regime Changes",
        "category": "Time Series",
        "difficulty": "Intermediate",
        "subtitle": "Stationarity assumptions, trends, unit roots, breaks, regimes, and state-dependent validation.",
    },
    "lotq-0029-time-series-basics-for-price-data.pdf": {
        "id": "LOTQ-0029",
        "title": "Time Series Basics for Price Data",
        "category": "Time Series",
        "difficulty": "Beginner",
        "subtitle": "Price series, return conventions, temporal dependence, baselines, and point-in-time pipelines.",
    },
    "lotq-0030-volatility-modeling-foundations.pdf": {
        "id": "LOTQ-0030",
        "title": "Volatility Modeling Foundations",
        "category": "Time Series",
        "difficulty": "Intermediate",
        "subtitle": "Volatility targets, conditional variance, realized variation, forecast validation, and capital controls.",
    },
    "lotq-0031-backtesting-biases-and-research-errors.pdf": {
        "id": "LOTQ-0031",
        "title": "Backtesting Biases and Research Errors",
        "category": "Backtesting",
        "difficulty": "Intermediate",
        "subtitle": "Audit causal, economic, statistical, and operational defects in historical research.",
    },
    "lotq-0032-backtesting-foundations-for-quant-research.pdf": {
        "id": "LOTQ-0032",
        "title": "Backtesting Foundations for Quant Research",
        "category": "Backtesting",
        "difficulty": "Beginner",
        "subtitle": "Build causal, executable, costed, reconciled, and independently validated simulations.",
    },
    "lotq-0033-data-cleaning-for-quant-research.pdf": {
        "id": "LOTQ-0033",
        "title": "Data Cleaning for Quant Research",
        "category": "Data Cleaning",
        "difficulty": "Beginner",
        "subtitle": "Classify data defects, apply conservative repairs, and preserve auditable evidence.",
    },
    "lotq-0034-data-pipelines-for-quant-research-systems.pdf": {
        "id": "LOTQ-0034",
        "title": "Data Pipelines for Quant Research Systems",
        "category": "Data Engineering",
        "difficulty": "Intermediate",
        "subtitle": "Build point-in-time, reproducible, testable, and reliable quantitative data pipelines.",
    },
    "lotq-0035-factor-signals-and-cross-sectional-ranking.pdf": {
        "id": "LOTQ-0035",
        "title": "Factor Signals and Cross-Sectional Ranking",
        "category": "Strategy Development",
        "difficulty": "Intermediate",
        "subtitle": "Construct comparable factor scores and map ranks into constrained portfolios.",
    },
    "lotq-0036-feature-engineering-for-trading-signals.pdf": {
        "id": "LOTQ-0036",
        "title": "Feature Engineering for Trading Signals",
        "category": "Feature Engineering",
        "difficulty": "Intermediate",
        "subtitle": "Create causal, stable, cost-aware features without leaking future information.",
    },
    "lotq-0037-forecasting-models-for-financial-time-series.pdf": {
        "id": "LOTQ-0037",
        "title": "Forecasting Models for Financial Time Series",
        "category": "Time Series",
        "difficulty": "Advanced",
        "subtitle": "Define forecast contracts, model uncertainty, and validate later predictive performance.",
    },
    "lotq-0038-labeling-targets-and-prediction-horizons.pdf": {
        "id": "LOTQ-0038",
        "title": "Labeling, Targets, and Prediction Horizons",
        "category": "Feature Engineering",
        "difficulty": "Intermediate",
        "subtitle": "Define causal outcomes and control leakage across overlapping prediction horizons.",
    },
    "lotq-0039-market-data-types-and-data-structures.pdf": {
        "id": "LOTQ-0039",
        "title": "Market Data Types and Data Structures",
        "category": "Data Engineering",
        "difficulty": "Beginner",
        "subtitle": "Recognize market-data objects and preserve identity, timing, and durable representations.",
    },
    "lotq-0040-mean-reversion-and-spread-based-signals.pdf": {
        "id": "LOTQ-0040",
        "title": "Mean Reversion and Spread-Based Signals",
        "category": "Strategy Development",
        "difficulty": "Intermediate",
        "subtitle": "Research temporary dislocations, convergence signals, spreads, and structural breaks.",
    },
    "lotq-0041-missing-data-outliers-and-bad-ticks.pdf": {
        "id": "LOTQ-0041",
        "title": "Missing Data, Outliers, and Bad Ticks",
        "category": "Data Cleaning",
        "difficulty": "Intermediate",
        "subtitle": "Separate valid market tails from defects and repair anomalies without inventing history.",
    },
    "lotq-0042-momentum-trend-and-breakout-signals.pdf": {
        "id": "LOTQ-0042",
        "title": "Momentum, Trend, and Breakout Signals",
        "category": "Strategy Development",
        "difficulty": "Intermediate",
        "subtitle": "Build and validate momentum, directional trend, and price-channel breakout signals.",
    },
    "lotq-0043-monte-carlo-simulation-for-strategy-testing.pdf": {
        "id": "LOTQ-0043",
        "title": "Monte Carlo Simulation for Strategy Testing",
        "category": "Simulation",
        "difficulty": "Advanced",
        "subtitle": "Generate plausible strategy paths and evaluate path dependence, tails, and uncertainty.",
    },
    "lotq-0044-pandas-and-numpy-for-market-data.pdf": {
        "id": "LOTQ-0044",
        "title": "Pandas and NumPy for Market Data",
        "category": "Python for Quant Research",
        "difficulty": "Beginner",
        "subtitle": "Turn market tables into aligned, causal, efficient, and reproducible analytical artifacts.",
    },
    "lotq-0045-python-foundations-for-quant-research.pdf": {
        "id": "LOTQ-0045",
        "title": "Python Foundations for Quant Research",
        "category": "Python for Quant Research",
        "difficulty": "Beginner",
        "subtitle": "Write clear, reproducible Python with sound timing and numerical integrity.",
    },
    "lotq-0046-research-databases-and-market-data-storage.pdf": {
        "id": "LOTQ-0046",
        "title": "Research Databases and Market Data Storage",
        "category": "Data Engineering",
        "difficulty": "Intermediate",
        "subtitle": "Design durable, point-in-time, query-efficient, recoverable quantitative data stores.",
    },
    "lotq-0047-signal-research-and-strategy-ideation.pdf": {
        "id": "LOTQ-0047",
        "title": "Signal Research and Strategy Ideation",
        "category": "Strategy Development",
        "difficulty": "Beginner",
        "subtitle": "Turn market observations into falsifiable hypotheses and traceable signal specifications.",
    },
    "lotq-0048-transaction-costs-slippage-and-liquidity.pdf": {
        "id": "LOTQ-0048",
        "title": "Transaction Costs, Slippage, and Liquidity",
        "category": "Backtesting",
        "difficulty": "Intermediate",
        "subtitle": "Connect spreads, impact, fill uncertainty, capacity, and costs to executable economics.",
    },
    "lotq-0049-vectorized-research-workflows-in-python.pdf": {
        "id": "LOTQ-0049",
        "title": "Vectorized Research Workflows in Python",
        "category": "Python for Quant Research",
        "difficulty": "Intermediate",
        "subtitle": "Build fast array workflows with explicit contracts, causal transforms, and reproducibility.",
    },
    "lotq-0050-walk-forward-testing-and-out-of-sample-validation.pdf": {
        "id": "LOTQ-0050",
        "title": "Walk-Forward Testing and Out-of-Sample Validation",
        "category": "Validation",
        "difficulty": "Intermediate",
        "subtitle": "Create deployment-like evidence with causal folds, frozen decisions, and model vintages.",
    },
}


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, width_chars: int, font: str, size: int, leading: int) -> float:
    c.setFont(font, size)
    for line in wrap(text, width_chars):
        c.drawString(x, y, line)
        y -= leading
    return y


def make_cover(meta: dict[str, str], width: float, height: float) -> bytes:
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.setFillColor(PAPER)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    margin = 48
    c.setFillColor(NAVY)
    c.roundRect(margin, height - 292, width - 2 * margin, 232, 14, fill=1, stroke=0)
    c.setFillColor(NAVY_2)
    c.roundRect(margin + 14, height - 326, width - 2 * margin - 28, 44, 10, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    eyebrow = f"{meta['id']} / {meta['category'].upper()} / {meta['difficulty'].upper()} / FIELD GUIDE"
    c.drawString(margin + 22, height - 92, eyebrow)

    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(margin + 22, height - 108, margin + 132, height - 108)

    y = height - 148
    c.setFillColor(colors.white)
    for line in wrap(meta["title"], 28):
        c.setFont("Helvetica-Bold", 30)
        c.drawString(margin + 22, y, line)
        y -= 36

    c.setFillColor(colors.HexColor("#DDE8F6"))
    y = draw_wrapped(c, meta["subtitle"], margin + 22, height - 262, 78, "Helvetica", 10, 14)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin + 28, height - 313, "Library of the Quant")
    c.setFont("Helvetica", 9)
    c.drawRightString(width - margin - 28, height - 313, "Educational reference manual")

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, height - 350, "Manual Profile")
    c.setStrokeColor(LINE)
    c.setLineWidth(1)
    c.line(margin, height - 360, width - margin, height - 360)

    profile = [
        ("Library ID", meta["id"]),
        ("Category", meta["category"]),
        ("Difficulty", meta["difficulty"]),
        ("Format", "Single-column field-guide manual"),
        ("Use", "Study, lookup, and research-system reference"),
    ]
    y = height - 392
    for label, value in profile:
        c.setFillColor(MUTED)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(margin, y, label.upper())
        c.setFillColor(INK)
        c.setFont("Helvetica", 11)
        c.drawString(margin + 110, y, value)
        y -= 26

    c.setFillColor(colors.HexColor("#E9EEF7"))
    c.roundRect(margin, 126, width - 2 * margin, 92, 10, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin + 18, 188, "Educational Use Only")
    c.setFont("Helvetica", 9)
    disclaimer = (
        "This manual is educational material for quant research study. It is not financial advice, "
        "not a trading recommendation, and not a guarantee of correctness or live trading usefulness."
    )
    draw_wrapped(c, disclaimer, margin + 18, 170, 88, "Helvetica", 9, 12)

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(margin, 54, f"Library of the Quant - {meta['title']}")
    c.drawRightString(width - margin, 54, meta["id"])
    c.showPage()
    c.save()
    packet.seek(0)
    return packet.read()


def normalize_pdf(pdf: Path) -> None:
    meta = MANUALS[pdf.name]
    reader = PdfReader(str(pdf))
    writer = PdfWriter()
    width = float(reader.pages[0].mediabox.width)
    height = float(reader.pages[0].mediabox.height)

    cover_reader = PdfReader(io.BytesIO(make_cover(meta, width, height)))
    writer.add_page(cover_reader.pages[0])

    for page in reader.pages[1:]:
        writer.add_page(page)

    tmp = pdf.with_suffix(".normalized.tmp.pdf")
    with tmp.open("wb") as fh:
        writer.write(fh)
    tmp.replace(pdf)


def main() -> None:
    for pdf in sorted(PDF_ROOT.rglob("*.pdf")):
        if pdf.name not in MANUALS:
            raise SystemExit(f"Missing metadata for {pdf}")
        normalize_pdf(pdf)
        print(f"normalized {pdf.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
