# t_beam_ex1.py
from xsect import t_beam_points, plot_section

points = t_beam_points(4, 3.5, 3/8, 1/2)
plot_section(points, title='T-Beam')
