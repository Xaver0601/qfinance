# Quantitative-Finance Basics
**This repo aims to cover some basics of quantitative finance.**

## Option Pricing Models
- Reads a ticker symbol from yahoo finance and analyzes the pricing of its call and put options. Includes interactive plots for visualizing how option prices change with different parameters.
- Supports [Black-Scholes](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model) and [Binomial Option Pricing Models (BOPM)](https://en.wikipedia.org/wiki/Binomial_options_pricing_model) for both European and American options.

- **Notebooks**: 
  - [demo.ipynb](options/demo.ipynb): Demo analysis of option pricing.
  - [interactive.ipynb](options/interactive.ipynb): Interactive plots comparing Black-Scholes and BOPM with sliders for parameters.

- TODO:
  - Store an example csv with data for close/call/put prices (yfinance is unreliable).
  - Properly compare Black-Scholes to BOPM.
  - Vectorize bopm.prob_of_profit().
  - More pricing models (Monte-Carlo?).
  - Analyze Greeks.
  - Analyze risk/return for known insider trades.

---

## Portfolio Optimization and Asset Allocation
- Evaluate risk/return profiles of stocks using metrics like alpha, beta, and Sharpe ratio.
- Analyze co-movement of stocks using correlation.
- Find optimal asset allocation to maximize sharpe ratio.

- **Notebooks**:
  - [compare.ipynb](portfolio/compare.ipynb): Compare risk/return profiles of stock vs benchmark (e.g. S&P 500) using alpha, beta, and Sharpe ratio.
  - [portfolio_construction.ipynb](portfolio/portfolio_construction.ipynb): Construct an optimal portfolio maximizing Sharpe ratio.

- TODO:
  - Find optimal asset allocations for e.g. maximum alpha, minimum volatility, etc.
  - Find uncorrelated stocks (maybe even negative correlation) to diversify risk.
  - Create own ETFs with different risk/return profiles and constraints (e.g. max 10% in any stock).

## Future topics to cover:
- Backtesting of strategies.
- Portfolio Optimization and Asset Allocation:
  - Markowitz model, Modern Portfolio Theory, etc.
- Quantitative Trading:
  - Predict market movements using statistics.
- Risk management:
  - Value at Risk (VaR), Expected Shortfall, etc.