using Random

function monte_carlo_option(S0, X, r, T, σ, num_paths=10000, option_type="call")
    dt = T  # Single step (since we're only looking at final price)
    W = randn(num_paths)  # Random normal values for Brownian motion
    ST = S0 * exp.((r - 0.5 * σ^2) * dt .+ σ * sqrt(dt) .* W)  # Simulated final prices

    if option_type == "call"
        payoffs = max.(ST .- X, 0)
    else
        payoffs = max.(X .- ST, 0)
    end

    return exp(-r * T) * mean(payoffs)  # Discounted expected payoff
end

# Example usage
S0 = 100   # Current stock price
X = 100    # Strike price
r = 0.05   # Risk-free rate
T = 1.0    # Time to maturity (in years)
σ = 0.2    # Volatility

# Example usage
mc_price = monte_carlo_option(S0, X, r, T, σ, 100000, "call")
println("Monte Carlo Call Option Price: $mc_price")
