from scipy.stats import norm
import numpy as np
from Option import Option


############ Black-Scholes-Model ############
# https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model


def N(x: float) -> float:
  '''
  Cumulative distribution function (CDF).
  '''
  return norm.cdf(x)


def dN(x: float) -> float:
  '''
  1st derivative of cumulative distribution function (CDF).
  '''
  return 1 / np.sqrt(2 * np.pi) * np.exp(-x**2 / 2)


def d_1(o: Option) -> float:
  '''
  Also 'd+' in literature.
  '''
  num = np.log(o.spot / o.strike) + (o.r + 0.5 * o.sigma**2) * o.tau
  denom = o.sigma * np.sqrt(o.tau)
  return num / denom


def d_2(o: Option) -> float:
  '''
  Also 'd-' in literature.
  '''
  return d_1(o) - o.sigma * np.sqrt(o.tau)


def option_price(o: Option) -> float:
  '''
  Option Price from Black-Scholes-Model.
  Parameters:
    o: Option object.
  '''
  if (o.type == 'call'):
    d1 = d_1(o)
    d2 = d_2(o)
    Ct = N(d1) * o.spot - N(d2) * o.strike * np.exp(-o.r * o.tau)
    return Ct
  else:
    d1 = d_1(o)
    d2 = d_2(o)
    Pt = N(-d2) * o.strike * np.exp(-o.r * o.tau) - N(-d1) * o.spot
    return Pt


def greeks(o: Option) -> tuple[float, float, float, float, float]:
  '''
  Returns 'The Greeks' of a given option.
  Parameters:
    o: Option object.
  Return:
    tuple: (delta, gamma, vega, theta, rho)
  '''
  d1 = d_1(o)
  d2 = d_2(o)
  gamma = dN(d1) / (o.spot * o.sigma * np.sqrt(o.tau))
  vega = o.spot * dN(d1) * np.sqrt(o.tau)

  if (o.type == 'call'):
    delta = N(d1)
    theta = -(o.spot * dN(d1) * o.sigma) / (2 * np.sqrt(o.tau)) - o.r * o.strike * np.exp(-o.r * o.tau) * N(d2)
    rho = o.strike * o.tau * np.exp(-o.r * o.tau) * N(d2)
  else:
    delta = N(d1) - 1
    theta = -(o.spot * dN(d1) * o.sigma) / (2 * np.sqrt(o.tau)) + o.r * o.strike * np.exp(-o.r * o.tau) * N(-d2)
    rho = -o.strike * o.tau * np.exp(-o.r * o.tau) * N(-d2)

  return delta, gamma, vega, theta, rho


# market_price = option_price(...sigma...)
# 0 = option_price - market_price
# f(x) = option_price - market_price
def find_iv(o: Option, sigma_init: float, price: float) -> float:
  '''
  Find implicit volatility (IV) using Newton-Raphson (max. 100 steps, Black-Scholes method).
  Parameters:
    o: Option object.
    sigma_init: Initial guess.
    price: Price of the Option.
  '''
  o.sigma = sigma_init
  for i in range(100):
    f = option_price(o) - price
    df = o.spot * dN(d_1(o)) * np.sqrt(o.tau)  # vega
    sigma_new = o.sigma - f / df
    if (np.abs(sigma_new - o.sigma) < 1e-5):
      return sigma_new
    o.sigma = sigma_new
  return np.nan


def prob_of_profit(o: Option) -> tuple[float, float]:
  '''
  Probability of Profit (POP) and being In-The-Money (ITM) for a given option.
  Parameters:
    o: Option object.
  Return:
    tuple: (POP, ITM)
  '''
  price = option_price(o)

  if (o.type == 'call'):
    d1 = 1 / (o.sigma * np.sqrt(o.tau)) * (np.log(o.spot / (o.strike + price)) + (o.r + o.sigma**2 / 2) * o.tau)
    d2 = d1 - o.sigma * np.sqrt(o.tau)
    return N(d2), N(d_2(o))
  else:
    d1 = 1 / (o.sigma * np.sqrt(o.tau)) * (np.log(o.spot / (o.strike - price)) + (o.r + o.sigma**2 / 2) * o.tau)
    d2 = d1 - o.sigma * np.sqrt(o.tau)
    return 1 - N(d2), 1 - N(d_2(o))


def expected_return(o: Option, mu: float) -> float:
  '''
  Expected return of an option.
  Parameters:
    o: Option object.
    mu: Expected return of the underlying asset.
  Return:
    Expected return of the option.
  '''
  price = option_price(o)
  delta, _, _, _, _ = greeks(o)
  omega = delta * o.spot / price
  return o.r + omega * (mu - o.r)
