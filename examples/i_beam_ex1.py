# i_beam_ex1.py
from xsect import i_beam_points, plot_section

points = i_beam_points(4, 3.5, 3/8, 1/2)
plot_section(points, title='I-Beam')
