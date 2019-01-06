# double_angle_ex1.py
from xsect import double_angle_points, multi_plot_section

points = double_angle_points(4, 3, 1/4, 1/4, 1/2)
multi_plot_section(points, title='Double Angle')
