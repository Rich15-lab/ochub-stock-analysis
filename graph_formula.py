import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Define the functions
def H(t):  # Human contribution
    return np.sin(t) + 1.5

def A(t):  # AI contribution
    return np.cos(t) + 1.5

def S(t):  # Synergy factor
    return np.log(t + 1) + 1

def K(t):  # Exponential growth factor
    return 0.5 * t

def formula(t):  # Combined formula
    return H(t) * A(t) * S(t) * np.exp(K(t))

# Generate the graph data
time = np.linspace(0, 10, 500)  # Time range
values = [formula(t) for t in time]

# Plot the graph
plt.figure(figsize=(8, 6))
plt.plot(time, values, label="Synergy Growth Over Time", linewidth=2)
plt.title("Dynamic Synergy Interaction Between Human and AI", fontsize=14)
plt.xlabel("Time (t)", fontsize=12)
plt.ylabel("Synergy Value", fontsize=12)
plt.grid(True)
plt.legend(fontsize=10)
plt.tight_layout()

# Show and save the graph
plt.savefig("synergy_graph.png", dpi=300)  # Save the graph as an image
plt.show()
