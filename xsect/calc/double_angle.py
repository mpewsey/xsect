from __future__ import division
from .angle import angle_points
from .multi import multi_section_summary

__all__ = ['double_angle_points', 'double_angle_summary']


def double_angle_points(leg1, leg2, thickness1, thickness2=None, separation=0):
    """
    Returns an array of double angle boundary points of shape (N, 2).

    Parameters
    ----------
    leg1 : float
        The length of the connected legs in the vertical direction.
    leg2 : float
        The length of the legs in the horizontal direction.
    thickness1 : float
        The thickness of `leg1`.
    thickness2 : float
        The thickness of `leg2`. If None, the thickness is assumed the same
        as `thickness1`.
    separation : float
        The separation distance between connected legs.
    """
    a = angle_points(leg1, leg2, thickness1, thickness2)
    a += (0.5*separation, 0)
    b = a * (-1, 1)
    return a, b


def double_angle_summary(leg1, leg2, thickness1, thickness2=None, separation=0):
    """
    Returns a dictionary with a summary of double angle properties.

    Parameters
    ----------
    leg1 : float
        The length of the connected legs in the vertical direction.
    leg2 : float
        The length of the legs in the horizontal direction.
    thickness1 : float
        The thickness of `leg1`.
    thickness2 : float
        The thickness of `leg2`. If None, the thickness is assumed the same
        as `thickness1`.
    separation : float
        The separation distance between connected legs.
    """
    p = double_angle_points(leg1, leg2, thickness1, thickness2, separation)
    return multi_section_summary(p)
