import numpy as np

class Option:
  def __init__(self, tau: float = 1.0, spot: float = 100.0, strike: float = 90.0, sigma: float = 0.2, r: float = 0.02, div: float = 0.0, type: str = 'call', region: str = 'eu'):
    '''
    Parameters:
      tau: Time to Maturity (years).
      spot: Spot price.
      strike: Exercise price.
      sigma: Volatility.
      r: risk-free return rate.
      div: dividend-yield.
      type: 'call' / 'put'.
      region: 'eu' / 'us'.
    '''
    # np.any in case of pandas series as input
    if (np.any(tau) < 0):
      raise ValueError("Invalid Time-To-Maturity (negative value)")
    if (np.any(spot) < 0):
      raise ValueError("Invalid Spot price (negative value)")
    if (np.any(strike) < 0):
      raise ValueError("Invalid Strike price (negative value)")
    if (np.any(sigma) < 0):
      raise ValueError("Invalid Volatility (negative value)")
    if (np.any(div) < 0):
      raise ValueError("Invalid Dividend-yield (negative value)")

    self.tau = tau
    self.spot = spot
    self.strike = strike
    self.sigma = sigma
    self.r = r
    self.div = div

    in_type = type.lower()
    if (in_type != 'call' and in_type != 'put'):
      raise ValueError("Invalid Option type")
    self.type = in_type

    in_region = region.lower()
    if (in_region != 'eu' and in_region != 'na'):
      raise ValueError("Invalid Option region")
    self.region = in_region

  def __str__(self):
    return f"tau: {self.tau}, spot: {self.spot}, strike: {self.strike}, sigma: {self.sigma}\nr: {self.r}, d: {self.div}, type: {self.type}, region: {self.region}"
