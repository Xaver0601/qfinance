import yfinance as yf
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta


def read_ticker(ticker: str, past: str = '2y', exp_days: int = 365) -> pd.DataFrame:
  '''
  Read call and put options from yahoo finance up to a given expiration date.
  Will use local data if it is available.
  Returns:
    Dataframes for [calls, puts, closing price], 'val'.
  Parameters:
    ticker: 4-character ticker symbol.
    past: Data range for volatility analysis.
    exp_days: Data range for option chain [days].
  '''
  # Get asset history and find historic volatility
  dat = yf.Ticker(ticker.upper())

  df = dat.history(period=past).reset_index()  # Reset so 'Date' is an actual column not just index
  df_close = df[['Date', 'Close']]
  df_close['Date'] = pd.to_datetime(df_close['Date'])

  TRADING_DAYS = 252
  returns = np.log(df_close['Close'] / df_close['Close'].shift(1)).dropna()
  returns.fillna(0, inplace=True)
  volatility = returns.rolling(window=TRADING_DAYS).std()  # daily volatility
  volatility = volatility * np.sqrt(TRADING_DAYS)  # annualized
  val = {'sigma': volatility.iloc[-1], 'spot': df_close['Close'].iloc[-1], 'r': 0.02, 'div': 0.0}

  current_date = datetime.datetime.today()
  # Filter so only options up to current_day + exp_days are used
  future_date = current_date + relativedelta(days=exp_days)
  option_dates = pd.to_datetime(dat.options)
  option_dates = option_dates[option_dates < future_date]
  option_dates = option_dates[option_dates > current_date]

  # Get option data
  df_c = pd.DataFrame()
  df_p = pd.DataFrame()
  calls_list = []
  puts_list = []
  for i in range(len(option_dates)):
    chain = dat.option_chain(dat.options[i])
    df_c_ = chain.calls
    df_p_ = chain.puts
    df_c_ = df_c_[['strike', 'bid', 'ask', 'lastPrice', 'volume', 'impliedVolatility']]
    df_p_ = df_p_[['strike', 'bid', 'ask', 'lastPrice', 'volume', 'impliedVolatility']]
    df_c_.insert(0, 'Exp.Date', option_dates[i])
    df_p_.insert(0, 'Exp.Date', option_dates[i])
    calls_list.append(df_c_)
    puts_list.append(df_p_)
  df_c = pd.concat(calls_list, ignore_index=True) if calls_list else pd.DataFrame()
  df_p = pd.concat(puts_list, ignore_index=True) if calls_list else pd.DataFrame()

  # Prepare extra columns
  if not df_c.empty:
    df_c.insert(1, 'TTM [d]', np.nan)
    df_c.insert(3, 'BS price (hist)', np.nan)
    df_c.insert(4, 'BS price (implied)', np.nan)
    df_c.insert(5, 'BOPM price (hist)', np.nan)
    df_c.insert(6, 'BOPM price (implied)', np.nan)
    df_c.insert(9, 'market', np.nan)
    df_c['TTM [d]'] = ((df_c['Exp.Date'] - current_date).dt.total_seconds()) / 86400 + 1
    df_c['market'] = np.abs(df_c['bid'] + df_c['ask']) / 2

  if not df_p.empty:
    df_p.insert(1, 'TTM [d]', np.nan)
    df_p.insert(3, 'BS price (hist)', np.nan)
    df_p.insert(4, 'BS price (implied)', np.nan)
    df_p.insert(5, 'BOPM price (hist)', np.nan)
    df_p.insert(6, 'BOPM price (implied)', np.nan)
    df_p.insert(9, 'market', np.nan)
    df_p['TTM [d]'] = ((df_p['Exp.Date'] - current_date).dt.total_seconds()) / 86400 + 1
    df_p['market'] = np.abs(df_p['bid'] + df_p['ask']) / 2

  if (df_c.empty or df_p.empty or df_close.empty):
    raise Warning("DataFrames are empty. Maybe data is outdated or try to increase exp_days")
  return df_c, df_p, df_close, val
