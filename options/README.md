### Call Option Example
- A call option is the right to buy a stock to a given price in the future. For example:
  - Current share price: 100€ (spot price)
  - Buy 1 call option for 15€ (premium; actual pricing based on volatility, risk-free rate, etc.) with strike price of 90€ and expiration in 1 year.
  - At expiration, the option can be exercised if the share price is above 90€ (in the money), or it can expire worthless if the share price is below 90€ (out of the money).

  - Scenario A: Share price increases to 150€ at expiration:
    - Regular share: Buy at 100€, sell at 150€ -> 50€ gain (50% return)
    - Call option: Buy for 15€, sell for 60€ (150-90) -> 45€ gain (300% return)
  - Scenario B: Share price decreases to 80€ at expiration:
    - Regular share: Buy at 100€, sell at 80€ -> 20€ loss (20% loss)
    - Call option: Buy for 15€, expires worthless -> 15€ loss (100% loss)

**You effectively control 1 share for only 15€ instead of 100€.**

---

### Put Option Example
- A put option is the right to sell a stock at a given price in the future. For example:
  - Current share price: 100€ (spot price)
  - Buy 1 put option for 10€ (premium) with strike price of 110€ and expiration in 1 year.
  - At expiration, the option can be exercised if the share price is below 110€ (in the money), or it can expire worthless if the share price is above 110€ (out of the money).

  - Scenario A: Share price increases to 120€ at expiration:
    - Regular share: Buy at 100€, sell at 120€ -> 20€ gain (20% return)
    - Put option: Buy for 10€, expires worthless -> 10€ loss (100% loss)
  - Scenario B: Share price decreases to 90€ at expiration:
    - Regular share: Buy at 100€, sell at 90€ -> 10€ loss (10% loss)
    - Put option: Buy for 10€, sell for 20€ (110-90) -> 10€ gain (100% return)