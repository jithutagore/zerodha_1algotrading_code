import random
import zerodha

# Define the reinforcement learning function
def reinforce(env, num_episodes, gamma, epsilon, learning_rate):
    # Initialize the Q-table with zeros
    q_table = {}
    
    # Initialize the balance to $10,000
    balance = 10000
    
    # Loop over the number of episodes
    for i in range(num_episodes):
        # Reset the environment for each episode
        obs = env.reset()
        
        # Initialize the total reward and done flag
        total_reward = 0
        done = False
        
        # Loop over the steps in the episode
        while not done:
            # Choose an action using an epsilon-greedy policy
            if random.uniform(0, 1) < epsilon:
                action = random.choice(env.action_space)
            else:
                if obs in q_table:
                    action = max(q_table[obs], key=q_table[obs].get)
                else:
                    action = random.choice(env.action_space)
            
            # Take a step in the environment and get the new observation, reward, and done flag
            new_obs, reward, done = balance_step(env, balance, action)
            
            # Update the Q-value for the previous state and action using the Q-learning update rule
            if obs not in q_table:
                q_table[obs] = {}
            if action not in q_table[obs]:
                q_table[obs][action] = 0
            q_table[obs][action] += learning_rate * (reward + gamma * max(q_table[new_obs].values()) - q_table[obs][action])
            
            # Update the total reward and current observation
            total_reward += reward
            obs = new_obs
        
        # Print the total reward for the episode
        print("Episode ", i, " completed with total reward of ", total_reward)
    
    # Return the learned Q-table
    return q_table

# Define the balance step function
def balance_step(env, balance, action):
    # Get the observation from the environment
    obs = env.get_observation()
    
    # Execute the action and get the order
    order = env.take_action(action)
    
    # Get the reward
    reward = env.get_reward(order)
    
    # Update the balance
    balance += reward
    
    # Check if the episode is done
    done = env.done()
    
    # Update the current step
    env.current_step += 1
    
    return obs, reward, done

# Create an instance of the Zeroth environment
env = zerodha.Zeroth()

# Define the hyperparameters
num_episodes = 1000
gamma = 0.9
epsilon = 0.1
learning_rate = 0.1

# Run the reinforcement learning algorithm
q_table = reinforce(env, num_episodes, gamma, epsilon, learning_rate)

# Save the learned Q-table to a file
with open('q_table.pickle', 'wb') as f:
    pickle.dump(q_table, f)
