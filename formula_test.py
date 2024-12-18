import numpy as np
from scipy.integrate import quad

# Define the components of the formula
def human_contribution(t):
    return np.log1p(t)

def ai_contribution(t):
    return np.sqrt(t)

def synergy_factor(t):
    return 0.5 * t

# Define the full formula
def formula(t):
    return human_contribution(t) * ai_contribution(t) * synergy_factor(t)

# Integrate the formula over a time range (0 to 10 as an example)
result, error = quad(formula, 0, 10)

print(f"Result of the formula integration: {result:.2f}")
