# cruciform_ex1.py
from xsect import cruciform_points, multi_plot_section

points = cruciform_points(2.5, 2.5, 1/4, 1/4, 1/2)
multi_plot_section(points, title='Cruciform')
