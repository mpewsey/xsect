from __future__ import division
import numpy as np
from .boundary import section_summary

__all__ = ['angle_points', 'angle_summary']


def angle_points(leg1, leg2, thickness1, thickness2=None):
    """
    Returns an array of angle boundary points of shape (N, 2).

    Parameters
    ----------
    leg1 : float
        The length of the leg in the vertical direction.
    leg2 : float
        The length of the leg in the horizontal direction.
    thickness1 : float
        The thickness of `leg1`.
    thickness2 : float
        The thickness of `leg2`. If None, the thickness is assumed the same
        as `thickness1`.
    """
    if thickness2 is None:
        thickness2 = thickness1

    p = [(0, 0), (leg2, 0), (leg2, thickness2), (thickness1, thickness2),
         (thickness1, leg1), (0, leg1), (0, 0)]
    return np.array(p, dtype='float')


def angle_summary(leg1, leg2, thickness1, thickness2=None):
    """
    Returns a dictionary with a summary of angle section properties.

    Parameters
    ----------
    leg1 : float
        The length of the leg in the vertical direction.
    leg2 : float
        The length of the leg in the horizontal direction.
    thickness1 : float
        The thickness of `leg1`.
    thickness2 : float
        The thickness of `leg2`. If None, the thickness is assumed the same
        as `thickness1`.
    """
    p = angle_points(leg1, leg2, thickness1, thickness2)
    return section_summary(p)
