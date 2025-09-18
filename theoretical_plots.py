import numpy as np
import matplotlib.pyplot as plt

# Define generation range
g = np.arange(1, 21)  # generations 1 (founder) through 20

# Define the two formulas
h_matrilinear = (3 * g -1) / (4*g-2)
h_patrilinear = (2 * (g * (g - 1)) + 1) / (g * (2 * g - 1))

# Plot 1: Matrilinear mitochondrial DNA and Patrilinear mitochondrial DNA
plt.figure(figsize=(7,5))
plt.plot(g, h_matrilinear, marker='o', label=r'$h_{mt,matrilinear}=\frac{3g-1}{4g-2}$')
# plt.title("Matrilinear mitochondrial DNA")
plt.plot(g, h_patrilinear, marker='s', color='orange', label=r'$h_{mt,patrilinear}=\frac{2(g(g-1))+1}{g(2g-1)}$')
plt.xlabel("Generations (g)")
plt.ylabel("$h_{mt}$")
plt.grid(True)
plt.legend()
plt.show()

