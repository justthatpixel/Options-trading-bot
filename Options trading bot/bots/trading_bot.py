import numpy as np
from scipy.stats import norm
from twilio.rest import Client

# Black-Scholes Model for Option Pricing
def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Calculate the Black-Scholes option price.
    
    Parameters:
        S (float): Current stock price
        K (float): Option strike price
        T (float): Time to expiration in years
        r (float): Risk-free interest rate (annual)
        sigma (float): Volatility of the underlying stock
        option_type (str): Type of option ('call' or 'put')

    Returns:
        float: The price of the option
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    return price

# Twilio API Configuration
def send_notification(body):
    """
    Send a notification using Twilio.

    Parameters:
        body (str): The message body to send
    """
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=body,
        from_='your_twilio_phone_number',
        to='your_phone_number'
    )
    
    print(f"Notification sent: {message.sid}")

# Example trading logic
def trading_bot(stock_price, strike_price, time_to_expiration, risk_free_rate, volatility):
    """
    A simple trading bot example using the Black-Scholes model.

    Parameters:
        stock_price (float): Current price of the stock
        strike_price (float): Strike price of the option
        time_to_expiration (float): Time to expiration in years
        risk_free_rate (float): Risk-free interest rate
        volatility (float): Volatility of the stock
    """
    call_price = black_scholes(stock_price, strike_price, time_to_expiration, risk_free_rate, volatility, 'call')
    print(f"Call Option Price: {call_price}")

    # Example condition: Notify if the call option price is above a threshold
    threshold = 10.0  # Example threshold
    if call_price > threshold:
        send_notification(f"Call option price is above threshold: ${call_price:.2f}")

# Parameters for the option
stock_price = 100.0       # Current stock price
strike_price = 95.0       # Option strike price
time_to_expiration = 0.5  # Time to expiration in years
risk_free_rate = 0.02     # Risk-free interest rate (2%)
volatility = 0.25         # Volatility (25%)

# Run the trading bot
trading_bot(stock_price, strike_price, time_to_expiration, risk_free_rate, volatility)
