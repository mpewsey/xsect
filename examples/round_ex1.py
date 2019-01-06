# round_ex1.py
import numpy as np
import matplotlib.pyplot as plt
from xsect import round_points, plot_section

fig = plt.figure(figsize=(7, 7))

# Round
ax1 = fig.add_subplot(221, title='Round', ylabel='Y', aspect='equal')
points = round_points(10)
plot_section(points, ax=ax1)

# Pipe
ax2 = fig.add_subplot(222, title='Pipe', aspect='equal')
points = round_points(10, 2)
plot_section(points, ax=ax2)

# Pacman
ax3 = fig.add_subplot(223, title='Pacman', xlabel='X', ylabel='Y', aspect='equal')
points = round_points(10, 5, start=25*np.pi/180, stop=335*np.pi/180)
plot_section(points, ax=ax3)

# Cut pipe
ax4 = fig.add_subplot(224, title='Cut Pipe', xlabel='X', aspect='equal')
points = round_points(10, 2, start=-80*np.pi/180, stop=40*np.pi/180)
plot_section(points, ax=ax4)
