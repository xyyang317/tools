import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 1))

# axes.set_xlim(0, 10)
axes.set_xticks(np.linspace(0, 10, 11))
axes.set_title("Subplot 2")
plt.grid(linestyle='-', axis='x', linewidth='1', color='black')

X= np.array([[9, 9, 0, 9, 0, 9, 9, 9, 0, 9, 10, 10]])
plt.imshow(X,cmap='Reds')
plt.tight_layout()
plt.show()