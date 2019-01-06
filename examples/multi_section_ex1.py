# multi_section_ex1.py
import numpy as np
import matplotlib.pyplot as plt
from xsect import round_points, multi_plot_section

fig = plt.figure(figsize=(7, 4))

# Vang plate
ax1 = fig.add_subplot(121, title='Vang Plate', xlabel='X', ylabel='Y', aspect='equal')

rect = np.array([(0, 0), (150, 0), (150, 60), (0, 60), (0, 0)])
circ1 = round_points(60, start=-np.pi/2, stop=np.pi/2) + (150, 30)
circ2 = round_points(30) + (150, 30)

multi_plot_section(add=[rect, circ1], subtract=[circ2], ax=ax1)

# Triangle cutout
ax2 = fig.add_subplot(122, title='Triangle Cutout', xlabel='X', aspect='equal')

rect = np.array([(0, 0), (330, 0), (330, 280), (0, 280), (0, 0)])
tri = np.array([(0, 0), (210, 0), (0, 210), (0, 0)]) + (50, 40)

multi_plot_section(add=[rect], subtract=[tri], ax=ax2)
