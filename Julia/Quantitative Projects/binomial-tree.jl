using Distributions

function binomial_tree(S0, X, r, T, σ, N, option_type="call")
    i = 0
    dt = T / N
    u = exp(σ * sqrt(dt))  # Up factor
    d = 1 / u              # Down factor
    p = (exp(r * dt) - d) / (u - d)  # Risk-neutral probability

    # Stock price tree
    stock_tree = [S0 * u^j * d^(i-j) for i in 0:N, j in 0:i]

    # Option values at maturity
    if option_type == "call"
        option_tree = max.(stock_tree[:, end] .- X, 0.0)
    else
        option_tree = max.(X .- stock_tree[:, end], 0.0)
    end
    # Backward induction
    for i in N-1:-1:0
        option_tree = exp(-r * dt) * (p * option_tree[1:end-1] + (1 - p) * option_tree[2:end])
    end

    return option_tree[1]
end


# Example usage
S0 = 100   # Current stock price
X = 100    # Strike price
r = 0.05   # Risk-free rate
T = 1.0    # Time to maturity (in years)
σ = 0.2    # Volatility

# Example usage
N = 100  # Number of steps
binomial_price = binomial_tree(S0, X, r, T, σ, N, "call")
println("Binomial Call Option Price: $binomial_price")