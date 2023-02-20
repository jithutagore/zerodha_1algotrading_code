import zerodha

# Define the momentum trading function
def momentum_trade(env, window_size, num_steps, threshold):
    # Initialize the balance to $10,000
    balance = 10000
    
    # Loop over the number of steps
    for i in range(num_steps):
        # Get the last n prices from the environment
        prices = env.get_prices(window_size)
        
        # Compute the momentum indicator
        momentum = (prices[-1] - prices[0]) / prices[0]
        
        # Take a long position if the momentum is above the threshold, otherwise take a short position
        if momentum > threshold:
            order = env.take_long_position()
        elif momentum < -threshold:
            order = env.take_short_position()
        else:
            order = None
        
        # Get the reward and update the balance
        if order is not None:
            reward = env.get_reward(order)
            balance += reward
        
        # Check if the episode is done
        done = env.done()
        
        # Update the current step
        env.current_step += 1
        
        if done:
            break
    
    # Return the final balance
    return balance

# Create an instance of the Zeroth environment
env = zerodha.Zeroth()

# Define the hyperparameters
window_size = 20
num_steps = 1000
threshold = 0.05

# Run the momentum trading strategy
final_balance = momentum_trade(env, window_size, num_steps, threshold)

# Print the final balance
print("Final balance: $", final_balance)
