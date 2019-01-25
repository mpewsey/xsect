from __future__ import division
import numpy as np
from .boundary import section_summary

__all__ = ['t_beam_points', 't_beam_summary']


def t_beam_points(height, width, flange_thickness, web_thickness):
    """
    Returns an array of T-beam boundary points of shape (N, 2).

    Parameters
    ----------
    height : float
        The height of the section.
    width : float
        The width of the section.
    flange_thickness : float
        The thickness of the horizontal flange.
    web_thickness : float
        The thickness of the vertical web.
    """
    x1 = 0.5*(width - web_thickness)
    x2 = x1 + web_thickness
    y1 = height - flange_thickness

    p = [(x1, 0), (x2, 0), (x2, y1), (width, y1), (width, height),
         (0, height), (0, y1), (x1, y1), (x1, 0)]

    return np.array(p, dtype='float')


def t_beam_summary(height, width, flange_thickness, web_thickness):
    """
    Returns a dictionary with a summary of T-beam section properties.

    Parameters
    ----------
    height : float
        The height of the section.
    width : float
        The width of the section.
    flange_thickness : float
        The thickness of the horizontal flange.
    web_thickness : float
        The thickness of the vertical web.
    """
    p = t_beam_points(height, width, flange_thickness, web_thickness)
    return section_summary(p)
