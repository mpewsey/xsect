# boundary_ex1.py
import numpy as np
import matplotlib.pyplot as plt
from xsect import plot_section

fig = plt.figure(figsize=(7, 4))

# Triangle
ax1 = fig.add_subplot(121, title='Triangle', xlabel='X', ylabel='Y', aspect='equal')
points = np.array([(0, 0), (10, 0), (2, 10), (0, 0)])

plot_section(points, ax=ax1)

# POW!
ax2 = fig.add_subplot(122, title='POW!', xlabel='X', ylabel='Y', aspect='equal')

np.random.seed(777777)
ang = np.sort(np.random.uniform(0, 2*np.pi, 100))
ro = np.random.uniform(5, 25, (100, 1))
points = ro * np.column_stack([np.cos(ang), np.sin(ang)])

plot_section(points, ax=ax2)
