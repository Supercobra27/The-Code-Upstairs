using Distributions

function black_scholes(S0, X, r, T, σ, option_type="call")
    d1 = (log(S0 / X) + (r + 0.5 * σ^2) * T) / (σ * sqrt(T))
    d2 = d1 - σ * sqrt(T)

    if option_type == "call"
        return S0 * cdf(Normal(), d1) - X * exp(-r * T) * cdf(Normal(), d2)
    else  # put option
        return X * exp(-r * T) * cdf(Normal(), -d2) - S0 * cdf(Normal(), -d1)
    end
end

# Example usage
S0 = 100   # Current stock price
X = 100    # Strike price
r = 0.05   # Risk-free rate
T = 1.0    # Time to maturity (in years)
σ = 0.2    # Volatility

call_price = black_scholes(S0, X, r, T, σ, "call")
put_price = black_scholes(S0, X, r, T, σ, "put")

println("Black-Scholes Call Price: $call_price")
println("Black-Scholes Put Price: $put_price")