from __future__ import division
import numpy as np
from .boundary import section_summary

__all__ = ['i_beam_points', 'i_beam_summary']


def i_beam_points(height, width, flange_thickness, web_thickness):
    """
    Returns an array of I-beam boundary points of shape (N, 2).

    Parameters
    ----------
    height : float
        The height of the section.
    width : float
        The width of the section and flanges.
    flange_thickness : float
        The flange thickness.
    web_thickness : float
        The web thickness.
    """
    x1 = 0.5*(width - web_thickness)
    x2 = x1 + web_thickness
    y1 = height - flange_thickness

    p = [(0, 0), (width, 0), (width, flange_thickness),
         (x2, flange_thickness), (x2, y1), (width, y1),
         (width, height), (0, height), (0, y1), (x1, y1),
         (x1, flange_thickness), (0, flange_thickness), (0, 0)]

    return np.array(p, dtype='float')


def i_beam_summary(height, width, flange_thickness, web_thickness):
    """
    Returns a dictionary with a summary of I-beam section properties.

    Parameters
    ----------
    height : float
        The height of the section.
    width : float
        The width of the section and flanges.
    flange_thickness : float
        The flange thickness.
    web_thickness : float
        The web thickness.
    """
    p = i_beam_points(height, width, flange_thickness, web_thickness)
    return section_summary(p)
