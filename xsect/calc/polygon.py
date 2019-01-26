from __future__ import division
import numpy as np
from .boundary import close_points, section_summary

__all__ = ['polygon_points', 'polygon_summary']


def polygon_points(n, radius, thickness=None, is_inscribed=True):
    """
    Returns an array of boundary points for a polygon.

    Parameters
    ----------
    n : int
        The number of sides to the polygon.
    radius : float
        The radius of the polygon.
    thickness : float
        The thickness of the wall. If None, the cross section will be assumed
        to be solid.
    is_inscribed : bool
        If True, an inscribed polygon will be generated for the specified
        radius. Otherwise, a circumscribed polygon will be generated.
    """
    c = np.cos(np.pi/n)

    if is_inscribed:
        ro = radius
    else:
        ro = radius / c

    ang = np.linspace(0.5*np.pi, 2.5*np.pi, n+1)
    ang = np.column_stack([np.cos(ang), np.sin(ang)])
    points = ro * ang

    if thickness is not None:
        if is_inscribed:
            ri = ro - thickness / c
        else:
            ri = (radius - thickness) / c

        p = ri * ang[::-1]
        points = np.concatenate([points, p])

    return close_points(points)


def polygon_summary(n, radius, thickness=None, is_inscribed=True):
    """
    Returns a dictionary with a summary of polygon section properties.

    Parameters
    ----------
    n : int
        The number of sides to the polygon.
    radius : float
        The radius of the polygon.
    thickness : float
        The thickness of the wall. If None, the cross section will be assumed
        to be solid.
    is_inscribed : bool
        If True, an inscribed polygon will be generated for the specified
        radius. Otherwise, a circumscribed polygon will be generated.
    """
    p = polygon_points(n, radius, thickness, is_inscribed)
    return section_summary(p)
