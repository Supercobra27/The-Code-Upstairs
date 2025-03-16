import matplotlib.pyplot as plt
import numpy as np

# Queue Parameters
service_rate = 0.75 # mu
arrival_rates = [0.2, 0.4, 0.5, 0.6, 0.65, 0.7, 0.72, 0.74, 0.745] # lambda

# Lists to store values
queue_length = []
queue_delay = []
queue_theory = []

# finding average delay here so L/lambda = W
def littlesLaw(avg_length, arrival):
    return avg_length / arrival

timeSlots = int(1e6)

for arrival_rate in arrival_rates:
    currQueue = 0
    avgQueue = 0
    
    # Theoretical Queueing Delay/Arrival Rate
    #rho = 1/(service_rate-arrival_rate)
    #queue_theory.append(rho)
    rho = (arrival_rate*(1-service_rate))/(service_rate*(1-arrival_rate))
    queue_theory.append((1/arrival_rate)*(rho/(1-rho)))
    
    pcktArrived = np.random.geometric(arrival_rate)
    pcktServiced = np.random.geometric(service_rate) if currQueue > 0 else float('inf')
    
    for time in range(timeSlots):
        
        # Packet has arrived
        if pcktArrived == 0:
           currQueue += 1
           pcktArrived = np.random.geometric(arrival_rate) # reset RV
           
           if currQueue == 1: # Start processing service time
               pcktServiced = np.random.geometric(service_rate) # reset RV
        
        # Packet gets serviced
        if pcktServiced == 0 and currQueue > 0:
           currQueue -= 1
           pcktServiced = np.random.geometric(service_rate) if currQueue > 0 else float('inf') # reset RV
        
        # Decrement Counters
        pcktArrived -= 1
        pcktServiced -= 1
        
        # Append for Avg Queue
        avgQueue += currQueue
    
    queue_length.append(avgQueue / timeSlots)
    queue_delay.append(littlesLaw(avgQueue / timeSlots, arrival_rate))
    
    
# Plt
plt.figure(figsize=(8, 5))
plt.plot(arrival_rates, queue_delay, 'bo-', label="Little's Law Delay")
plt.plot(arrival_rates, queue_theory, 'ro--', label="Theoretical Delay")
plt.xlabel("Arrival Rate")
plt.ylabel("Expected Queueing Delay")
plt.title("Simulated Delay vs. Arrival Rate")
plt.legend()
plt.grid()
plt.show()