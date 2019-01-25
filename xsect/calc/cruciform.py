from __future__ import division
from .angle import angle_points
from .multi import multi_section_summary

__all__ = ['cruciform_points', 'cruciform_summary']


def cruciform_points(leg1, leg2, thickness1, thickness2=None, separation=0):
    """
    Returns an array of cruciform boundary points of shape (N, 2).

    Parameters
    ----------
    leg1 : float
        The length of the legs in the vertical direction.
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
    a += (0.5*separation, 0.5*separation)
    b = a * (-1, 1)
    c = a * (1, -1)
    d = a * (-1, -1)
    return a, b, c, d


def cruciform_summary(leg1, leg2, thickness1, thickness2=None, separation=0):
    """
    Returns a dictionary with a summary of cruciform properties.

    Parameters
    ----------
    leg1 : float
        The length of the legs in the vertical direction.
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
    p = cruciform_points(leg1, leg2, thickness1, thickness2, separation)
    return multi_section_summary(p)
