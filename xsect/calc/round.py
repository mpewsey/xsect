from __future__ import division
import numpy as np
from .boundary import close_points, section_summary

__all__ = ['round_area', 'round_inertia', 'round_gyradius',
           'round_sect_mod', 'round_points', 'round_summary']


def round_area(diameter, thickness=None):
    """
    Returns the cross sectional area for a round or pipe.

    Parameters
    ----------
    diameter : float
        The outside diameter of the round or pipe.
    thickness : float
        The thickness of the pipe. If None, the cross section is assumed
        to be a solid round.
    """
    ro = 0.5 * diameter

    if thickness is None:
        return np.pi*ro**2

    ri = ro - thickness

    return np.pi*(ro**2 - ri**2)


def round_inertia(diameter, thickness=None):
    """
    Returns the area inertia for a round or pipe.

    Parameters
    ----------
    diameter : float
        The outside diameter of the round or pipe.
    thickness : float
        The thickness of the pipe. If None, the cross section is assumed
        to be a solid round.
    """
    ro = 0.5 * diameter

    if thickness is None:
        return 0.25*np.pi*ro**4

    ri = ro - thickness

    return 0.25*np.pi*(ro**4 - ri**4)


def round_gyradius(diameter, thickness=None):
    """
    Returns the radius of gyration for a round or pipe.

    Parameters
    ----------
    diameter : float
        The outside diameter of the round or pipe.
    thickness : float
        The thickness of the pipe. If None, the cross section is assumed
        to be a solid round.
    """
    i = round_inertia(diameter, thickness)
    a = round_area(diameter, thickness)
    return (i / a)**0.5


def round_sect_mod(diameter, thickness=None):
    """
    Returns the section modulus for a round or pipe.

    Parameters
    ----------
    diameter : float
        The outside diameter of the round or pipe.
    thickness : float
        The thickness of the pipe. If None, the cross section is assumed
        to be a solid round.
    """
    i = round_inertia(diameter, thickness)
    c = 0.5 * diameter
    return i / c


def round_points(diameter, thickness=None, start=0, stop=2*np.pi, step=0.01):
    """
    Returns an array of boundary points for a round or pipe.

    Parameters
    ----------
    diameter : float
        The outside diameter of the round or pipe.
    thickness : float
        The wall thickness of the pipe. If None, the cross section will
        be assumed to be solid.
    start : float
        The starting angle for point generation, in radians.
    stop : float
        The ending angle for point generation, in radians.
    step : float
        The step interval for point generation. A smaller value will
        provide a boundary closer to that of the ideal shape at the expense
        of more memory and computation time.
    """
    ro = 0.5 * diameter
    n = int(np.ceil(abs(ro * (stop - start) / step)))
    if n < 2: n = 2
    ang = np.linspace(start, stop, n)
    points = ro * np.column_stack([np.cos(ang), np.sin(ang)])

    if thickness is not None:
        ri = ro - thickness
        n = int(np.ceil(abs(ri * (stop - start) / step)))
        if n < 2: n = 2
        ang = np.linspace(stop, start, n)
        p = ri * np.column_stack([np.cos(ang), np.sin(ang)])
        points = np.concatenate([points, p])

    return close_points(points)


def round_summary(diameter, thickness=None, start=0, stop=2*np.pi, step=0.01):
    """
    Returns a dictionary with a summary of cross sectional properties
    for the round. If the `start` and `stop` angles represent a closed ring,
    then the values returned are exact. Otherwise, the values will be
    approximated based on boundary point calculations.

    Parameters
    ----------
    diameter : float
        The outside diameter of the round or pipe.
    thickness : float
        The wall thickness of the pipe. If None, the cross section will
        be assumed to be solid.
    start : float
        The starting angle for point generation, in radians.
    stop : float
        The ending angle for point generation, in radians.
    step : float
        The step interval for point generation. A smaller value will
        provide a boundary closer to that of the ideal shape at the expense
        of more memory and computation time.

    Returns
    -------
    area : float
        The cross sectional area.
    x, y : float
        The x and y centroid coordinates.
    interia_x, inertia_y : float
        The moment of inertias about the x and y axes.
    inertia_j : float
        The polar moment of inertia.
    inertia_xy : float
        The product of inertia.
    inertia_z : float
        The moment of inertias about the weak principal axis.
    gyradius_x, gyradius_y : float
        The radii of gyrations about the x and y axes.
    gyradius_z : float
        The radii of gyrations about the weak principal axis.
    elast_sect_mod_x, elast_sect_mod_y : float
        The elastic section modulii about the x and y axes.
    elast_sect_mod_z : float
        The elastic section modulus about the weak principal axis.
    """
    if start == 0 and stop == 2*np.pi:
        a = round_area(diameter, thickness)
        i = round_inertia(diameter, thickness)
        ij = 2 * i
        r = round_gyradius(diameter, thickness)
        s = round_sect_mod(diameter, thickness)

        summary = dict(
            area=a, x=0, y=0, width=diameter/2, height=diameter/2,
            inertia_x=i, inertia_y=i, inertia_j=ij, inertia_xy=0, inertia_z=i,
            gyradius_x=r, gyradius_y=r, gyradius_z=r,
            elast_sect_mod_x=s, elast_sect_mod_y=s, elast_sect_mod_z=s
        )

        return summary

    p = round_points(diameter, thickness, start, stop, step)
    return section_summary(p)
