import yfinance as yf
import pandas as pd
import numpy as np


def read_ticker(ticker: list[str], past: str = '2y') -> pd.DataFrame:
  '''
  Read daily closing prices for a list of ticker symbols from yahoo finance.
  Returns:
    DataFrame: idx: Date, cols: {ticker}_Close
  Parameters:
    ticker: List of ticker symbols.
    past: Data range.
  '''
  df = pd.DataFrame()
  for t in ticker:
    df_t = yf.Ticker(t.upper()).history(period=past, auto_adjust=False)
    df_t = df_t[['Adj Close']].tz_localize(None)  # include dividends and splits
    df_t.columns = [f'{t}_Close']
    df = pd.concat([df, df_t], axis=1)
  return df


def read_risk_free(fed_path: str = 'fed_rates.csv', ecb_path: str = 'ecb_rates.csv') -> pd.DataFrame:
  '''
  Read risk free rates from csv files.
  Returns:
    DataFrames for FED and ECB rates.
  Parameters:
    fed_path: Path to FED rates csv file.
    ecb_path: Path to ECB rates csv file.
  '''
  # https://www.macrotrends.net/2015/fed-funds-rate-historical-chart
  df_fed = pd.read_csv(fed_path, delimiter=';', decimal=',', index_col=0)
  df_fed.index = pd.to_datetime(df_fed.index)
  df_fed.columns = ['FED_rate']

  # https://data.ecb.europa.eu/main-figures/ecb-interest-rates-and-exchange-rates/key-ecb-interest-rates?tab=Key+ECB+interest+rates&indicator=Key+ECB+interest+rates
  df_ecb = pd.read_csv(ecb_path, delimiter=',', index_col=0)
  df_ecb.index.name = 'Date'
  df_ecb.index = pd.to_datetime(df_ecb.index)
  df_ecb.drop(df_ecb.columns[0], axis=1, inplace=True)  # drop first column (redundant date column)
  df_ecb.columns = ['ECB_deposit_rate', 'ECB_marginal_lending_rate', 'ECB_rate']
  df_ecb = df_ecb[['ECB_rate']]
  return df_fed, df_ecb


def annualized_return(se: pd.Series) -> float:
  '''
  Calculate the annualized return of a price series.
  Returns:
    Annualized return.
  Parameters:
    se: Price series.
  '''
  # compound_growth = se.iloc[-1] / se.iloc[-window+1]
  # daily_growth = compound_growth**(1 / window)
  compound_growth = se.iloc[-1] / se.iloc[0]
  daily_growth = compound_growth**(1 / len(se))
  return daily_growth**252 - 1


def annualized_vol(se: pd.Series, window: int = 21) -> pd.Series:
  '''
  Calculate the annualized volatility of a price series at each point in time given a time window.
  Returns:
    Annualized volatility as a Series.
  Parameters:
    se: Price series.
    window: Rolling window size.
  '''
  returns = np.log(se / se.shift(1)).fillna(0)
  sigma = returns.rolling(window=window).std().fillna(0)  # daily volatility
  return sigma * np.sqrt(252)  # annualized volatility


def sharpe_ratio(ret: pd.Series, rf: pd.Series) -> float:
  '''
  Calculate the annualized Sharpe ratio of a return series given a risk free rate series.
  Returns:
    Annualized Sharpe ratio as a float.
  Parameters:
    ret: Return series.
    rf: Risk free rate series.
  '''
  excess_return = ret - np.log(1 + rf / 100 / 252)
  return excess_return.mean() / excess_return.std() * np.sqrt(252)


def risk_params(df: pd.DataFrame, ticker: str, ref: str, rf: pd.Series) -> tuple[float, float]:
  '''
  Calculate the beta and alpha of a stock given a reference index and risk free rate.
  Returns:
    Tuple of beta and alpha.
  Parameters:
    df: DataFrame containing the price data for the stock and reference index.
    ticker: Ticker symbol of the stock.
    ref: Ticker symbol of the reference index.
    rf: Risk free rate series.
  '''
  covariance = df[f'{ticker}_Returns'].cov(df[f'{ref}_Returns'])
  market_variance = df[f'{ref}_Returns'].var()
  beta = covariance / market_variance

  returns_ann = annualized_return(df[f'{ticker}_Close'])
  market_ann = annualized_return(df[f'{ref}_Close'])
  mean_FED_rate = rf.mean() / 100
  alpha = returns_ann - (mean_FED_rate + beta * (market_ann - mean_FED_rate))  # actual return - expected return
  return beta, alpha
