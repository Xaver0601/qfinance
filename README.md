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

## Future topics to cover:
- Backtesting of strategies.
- Portfolio Optimization and Asset Allocation:
  - Markowitz model, Modern Portfolio Theory, etc.
  - Analyze risk/return profiles of stocks (alpha, beta, sharpe ratio, etc.).
  - Find correlated stocks and analyze their co-movement (correlation, cointegration, etc.).
- Quantitative Trading:
  - Predict market movements using statistics.
- Risk management:
  - Value at Risk (VaR), Expected Shortfall, etc.