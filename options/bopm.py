from scipy.stats import binom
import numpy as np
from Option import Option


############ Binomial Options Pricing Model (BOPM) ############
# https://en.wikipedia.org/wiki/Binomial_options_pricing_model


# Supports scalar and pandas series input (Gemini).
def option_price(o: Option, n: int = 100):
  '''
  Option Price from Binomial Tree Model.
  Handles both scalar inputs and Pandas Series/Numpy Array inputs.
  Parameters:
    o: Option object.
    n: number of tree-levels.
  '''
  # TODO: Understand this more

  # 1. Helper: Ensure inputs are Column Vectors (M, 1) if they are arrays.
  # This allows them to broadcast against the Row Vector (1, N) of tree steps.
  def _to_col(x):
    x = np.asarray(x)
    # If it's a scalar (ndim=0), leave it alone. If it's a vector (ndim>0), make it (M, 1)
    return x[:, None] if x.ndim > 0 else x

  # Prepare parameters for broadcasting
  tau = _to_col(o.tau)
  spot = o.spot
  strike = _to_col(o.strike)
  sigma = _to_col(o.sigma)
  r = o.r
  div = o.div

  dt = tau / n

  # These calculations now result in either scalars or (M, 1) arrays
  u = np.exp(sigma * np.sqrt(dt))
  d = 1 / u
  p = (np.exp((r - div) * dt) - d) / (u - d)

  # 2. Reshape tree steps to Row Vector (1, N+1)
  # This ensures: (M, 1) * (1, N) = (M, N) matrix
  j = np.arange(n + 1).reshape(1, -1)

  # asset_prices is now shape (M, n+1) (or (n+1,) if scalar)
  asset_prices = spot * (u ** (n - j)) * (d ** j)

  # Find option price at expiration date
  if (o.type == 'call'):
    option_values = np.maximum(asset_prices - strike, 0)
  elif (o.type == 'put'):
    option_values = np.maximum(strike - asset_prices, 0)

  # Go backwards to find option price at start
  for i in range(n - 1, -1, -1):
    # 3. Use Ellipsis (...) slicing
    # This handles both 1D (scalar input) and 2D (vector input) arrays correctly.
    # It slices the LAST dimension (the time steps).
    option_values = np.exp(-r * dt) * (p * option_values[..., :-1] + (1 - p) * option_values[..., 1:])

    if (o.region == 'us'):
      # Recreate the asset price tree at step i
      # j must be trimmed to match the current step count (i+1)
      j_curr = np.arange(i + 1).reshape(1, -1)

      current_assets = spot * (u ** (i - j_curr)) * (d ** j_curr)

      if o.type == 'call':
        exercise = np.maximum(current_assets - strike, 0)
      else:
        exercise = np.maximum(strike - current_assets, 0)

      option_values = np.maximum(option_values, exercise)

  # If the input was a Series/array, option_values is now shape (M, 1).
  # We flatten it back to (M,) for cleaner output.
  if option_values.ndim > 1:
    return option_values.flatten()

  return option_values.item()  # Return float if scalar


# Does not support pandas series as input but more optimized (Gemini).
def option_price_old(o: Option, n: int = 100) -> float:
  '''
  Option Price from Binomial Tree Model.
  Does not support Pandas Series as input.
  Parameters:
    o: Option object.
    n: number of tree-levels.
  '''
  dt = o.tau / n
  # assert (dt < (o.sigma**2) / (o.r - o.div)**2)

  u = np.exp(o.sigma * np.sqrt(dt))
  d = 1 / u
  p = (np.exp((o.r - o.div) * dt) - d) / (u - d)

  # Brownian step tree, only last step required
  j = np.arange(n + 1)  # Number of down steps
  asset_prices = o.spot * (u ** (n - j)) * (d ** j)

  # Find option price at expiration date
  if (o.type == 'call'):
    option_values = np.maximum(asset_prices - o.strike, 0)
  elif (o.type == 'put'):
    option_values = np.maximum(o.strike - asset_prices, 0)

  # Go backwards to find option price at start
  for i in range(n - 1, -1, -1):
    # TODO: understand this step
    option_values = np.exp(-o.r * dt) * (p * option_values[:-1] + (1 - p) * option_values[1:])

    if (o.region == 'us'):
      current_assets = o.spot * (u ** (i - np.arange(i + 1))) * (d ** np.arange(i + 1))  # recalculate final spot prices
      if o.type == 'call':
        exercise = np.maximum(current_assets - o.strike, 0)
      else:
        exercise = np.maximum(o.strike - current_assets, 0)
      option_values = np.maximum(option_values, exercise)

  return option_values[0]


# Does not support pandas series as input but more intuitive to understand and implement.
def option_price_old_old(o: Option, n: int = 100) -> float:
  '''
  Option Price from Binomial Tree Model.
  Does not support Pandas Series as input.
  Parameters:
    o: Option object.
    n: number of tree-levels.
  '''
  dt = o.tau / n
  # assert (dt < (o.sigma**2) / (o.r - o.div)**2)

  u = np.exp(o.sigma * np.sqrt(dt))
  d = 1 / u
  p = (np.exp((o.r - o.div) * dt) - d) / (u - d)

  # Brownian step tree
  asset = np.zeros((n + 1, n + 1))
  for i in range(n + 1):  # timestep
    for j in range(i + 1):  # down-moves
      # price = spot * (u^up-moves) * (d^down-moves); up-moves = total-moves (i) - down-moves (j)
      asset[j, i] = o.spot * (u ** (i - j)) * (d ** j)

  # Find option price at expiration date
  if (o.type == 'call'):
    asset[:, -1] = np.maximum(asset[:, -1] - o.strike, 0)
  else:
    asset[:, -1] = np.maximum(o.strike - asset[:, -1], 0)

  # Go backwards to find option price at start
  for i in range(n - 1, -1, -1):
    for j in range(i + 1):
      bival = np.exp(-o.r * dt) * (p * asset[j, i + 1] + (1 - p) * asset[j + 1, i + 1])

      if (o.region == 'us'):
        exercise_value = np.maximum(asset[j, i] - o.strike, 0)
        bival = np.maximum(bival, exercise_value)

      asset[j, i] = bival

  return asset[0][0]


def prob_of_profit(o: Option, mu: float, n: int = 100) -> float:
  '''
  Probability of Profit (POP) and being In-The-Money (ITM) for a given option.
  Parameters:
    o: Option object.
    mu: Expected return of asset.
    n: Number of tree-levels.
  Return:
    POP, ITM
  '''
  price = option_price(o, n)
  dt = o.tau / n

  u = np.exp(o.sigma * np.sqrt(dt))
  d = 1 / u

  # Brownian step tree, only final nodes, final outcome only dependent on volatility
  j = np.arange(n + 1)
  final_spot = o.spot * (u ** (n - j)) * (d ** j)

  # How many outcomes are profitable?
  if o.type == 'call':
    is_itm = final_spot > (o.strike)
    payoff = np.maximum(final_spot - o.strike, 0)
  else:
    is_itm = final_spot < (o.strike)
    payoff = np.maximum(o.strike - final_spot, 0)
  is_profitable = payoff > (price * np.exp(o.r * o.tau))

  # Binomial distribution using 'real' probability with expected return
  p_real = (np.exp(mu * dt) - d) / (u - d)

  probabilites = binom.pmf(j, n, p_real)
  pop = np.sum(probabilites[is_profitable])
  itm = np.sum(probabilites[is_itm])
  return pop, itm
