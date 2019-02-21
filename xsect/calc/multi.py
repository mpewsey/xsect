from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from .boundary import TOL, area, centroid, inertias, close_points, rotate2

__all__ = [
    'multi_dimensions',
    'multi_area',
    'multi_centroid',
    'multi_inertias',
    'multi_principal_inertias',
    'multi_principal_angles',
    'multi_gyradii',
    'multi_principal_gyradii',
    'multi_extreme_fibers',
    'multi_principal_extreme_fibers',
    'multi_elast_sect_mod',
    'multi_principal_elast_sect_mod',
    'multi_plot_section',
    'multi_section_summary'
]


def multi_dimensions(add):
    """
    Returns the width and height of the section defined by the input boundary
    points.

    Parameters
    ----------
    add : array
        An array of (x, y) coordinates of shape (N, 2).
    """
    mn = np.array([np.min(x, axis=0) for x in add])
    mx = np.array([np.max(x, axis=0) for x in add])
    mn, mx = np.min(mn, axis=0), np.max(mx, axis=0)
    return mx - mn


def multi_area(add, subtract=[]):
    """
    Returns the total cross sectional area for multiple shapes.

    Parameters
    ----------
    add : list
        A list of (x, y) boundary coordinates for shapes included in the
        cross section. Each set of boundary coordinates should be of the
        shape (N, 2).
    subtract : list
        A list of (x, y) boundary coordinates for cut out shapes to be
        subtracted from the cross section. Each set of boundary coordinates
        should be of the shape (N, 2).
    """
    a_add = sum(area(x) for x in add)
    a_sub = sum(area(x) for x in subtract)
    return a_add - a_sub


def multi_centroid(add, subtract=[]):
    """
    Returns the centroid for cross sections including multiple shapes.
    Returns an array of shape (2,).

    Parameters
    ----------
    add : list
        A list of (x, y) boundary coordinates for shapes included in the
        cross section. Each set of boundary coordinates should be of the
        shape (N, 2).
    subtract : list
        A list of (x, y) boundary coordinates for cut out shapes to be
        subtracted from the cross section. Each set of boundary coordinates
        should be of the shape (N, 2).
    """
    # Added areas
    a = np.array([area(x) for x in add])
    a = np.expand_dims(a, 1)
    c = np.array([centroid(x) for x in add])

    cx = np.sum(a * c, axis=0)
    cy = np.sum(a)

    # Subtracted areas
    if len(subtract) > 0:
        a = np.array([area(x) for x in subtract])
        a = np.expand_dims(a, 1)
        c = np.array([centroid(x) for x in subtract])

        cx -= np.sum(a * c, axis=0)
        cy -= np.sum(a)

    return cx / cy


def multi_inertias(add, subtract=[], origin=None):
    """
    Calculates the area moment of inertias for cross sections including
    multiple shapes. Returns an array of shape (4,).

    Parameters
    ----------
    add : list
        A list of (x, y) boundary coordinates for shapes included in the
        cross section. Each set of boundary coordinates should be of the
        shape (N, 2).
    subtract : list
        A list of (x, y) boundary coordinates for cut out shapes to be
        subtracted from the cross section. Each set of boundary coordinates
        should be of the shape (N, 2).
    origin : array
        The (x, y) origin about which the moment of inertias will be calculated.
        The array should be of the shape (2,). If None, the origin will be
        assumed to be located at the centroid of the section.

    Returns
    -------
    inertia_x : float
        The moment of inertia about the x-axis.
    inertia_y : float
        The moment of inertia about the y-axis.
    inertia_j : float
        The polar moment of inertia.
    inertia_xy : float
        The product of inertia.
    """
    if origin is None:
        origin = multi_centroid(add, subtract)

    def inertia(points):
        if len(points) == 0:
            return np.zeros(4)
        i = np.array([inertias(x, origin) for x in points])
        return np.sum(i, axis=0)

    a = inertia(add)
    b = inertia(subtract)

    return a - b


def multi_principal_inertias(add, subtract=[]):
    """
    Calculates the principal area moment of inertias for multiple shapes.
    Returns an array of shape (2,).

    Parameters
    ----------
    add : list
        A list of (x, y) boundary coordinates for shapes included in the
        cross section. Each set of boundary coordinates should be of the
        shape (N, 2).
    subtract : list
        A list of (x, y) boundary coordinates for cut out shapes to be
        subtracted from the cross section. Each set of boundary coordinates
        should be of the shape (N, 2).
    """
    ix, iy, ij, ixy = multi_inertias(add, subtract)
    avg = 0.5*ij
    diff = 0.5*(ix - iy)
    diff = (diff**2 + ixy**2)**0.5
    iu, iv = avg + diff, avg - diff
    return np.array([iu, iv])


def multi_principal_angles(add, subtract=[]):
    """
    Calculates the angles from the x-axis to the principal axes. Returns
    array of shape (2,).

    Parameters
    ----------
    add : list
        A list of (x, y) boundary coordinates for shapes included in the
        cross section. Each set of boundary coordinates should be of the
        shape (N, 2).
    subtract : list
        A list of (x, y) boundary coordinates for cut out shapes to be
        subtracted from the cross section. Each set of boundary coordinates
        should be of the shape (N, 2).
    """
    ix, iy, _, ixy = multi_inertias(add, subtract)
    diff = ix - iy

    if abs(ixy) < TOL and abs(diff) < TOL:
        alpha = 0
    else:
        alpha = 0.5*np.arctan2(-ixy, 0.5*diff)

    beta = alpha + np.pi/2
    return np.array([alpha, beta])


def multi_gyradii(add, subtract=[]):
    """
    Calculates the radii of gyrations about the x and y axes. Returns
    an array of shape (2,).

    Parameters
    ----------
    add : list
        A list of (x, y) boundary coordinates for shapes included in the
        cross section. Each set of boundary coordinates should be of the
        shape (N, 2).
    subtract : list
        A list of (x, y) boundary coordinates for cut out shapes to be
        subtracted from the cross section. Each set of boundary coordinates
        should be of the shape (N, 2).
    """
    a = multi_area(add, subtract)
    i = multi_inertias(add, subtract)[:2]
    return np.sqrt(i / a)


def multi_principal_gyradii(add, subtract=[]):
    """
    Calculates the radii of gyrations about the principal axes. Returns
    an array of shape (2,).

    Parameters
    ----------
    add : list
        A list of (x, y) boundary coordinates for shapes included in the
        cross section. Each set of boundary coordinates should be of the
        shape (N, 2).
    subtract : list
        A list of (x, y) boundary coordinates for cut out shapes to be
        subtracted from the cross section. Each set of boundary coordinates
        should be of the shape (N, 2).
    """
    a = multi_area(add, subtract)
    i = multi_principal_inertias(add, subtract)[:2]
    return np.sqrt(i / a)


def multi_extreme_fibers(add, subtract=[]):
    """
    Calculates the extreme fibers from the x and y axes. Returns an array
    of shape (2,).

    Parameters
    ----------
    add : list
        A list of (x, y) boundary coordinates for shapes included in the
        cross section. Each set of boundary coordinates should be of the
        shape (N, 2).
    subtract : list
        A list of (x, y) boundary coordinates for cut out shapes to be
        subtracted from the cross section. Each set of boundary coordinates
        should be of the shape (N, 2).
    """
    c = multi_centroid(add, subtract)
    c = np.array([np.max(np.abs(x - c), axis=0) for x in add])
    c = np.max(c, axis=0)
    return np.flip(c, axis=0)


def multi_principal_extreme_fibers(add, subtract=[]):
    """
    Calculates the extreme fibers from the principal axes. Returns an array
    of shape (2,).

    Parameters
    ----------
    add : list
        A list of (x, y) boundary coordinates for shapes included in the
        cross section. Each set of boundary coordinates should be of the
        shape (N, 2).
    subtract : list
        A list of (x, y) boundary coordinates for cut out shapes to be
        subtracted from the cross section. Each set of boundary coordinates
        should be of the shape (N, 2).
    """
    alpha, _ = multi_principal_angles(add, subtract)
    c = multi_centroid(add, subtract)
    c = [np.max(np.abs(rotate2(x - c, alpha)), axis=0) for x in add]
    c = np.max(np.array(c), axis=0)
    return np.flip(c, axis=0)


def multi_elast_sect_mod(add, subtract=[]):
    """
    Calculates the section modulii about the x and y axes. Returns an array
    of shape (2,).

    Parameters
    ----------
    add : list
        A list of (x, y) boundary coordinates for shapes included in the
        cross section. Each set of boundary coordinates should be of the
        shape (N, 2).
    subtract : list
        A list of (x, y) boundary coordinates for cut out shapes to be
        subtracted from the cross section. Each set of boundary coordinates
        should be of the shape (N, 2).
    """
    i = multi_inertias(add, subtract)[:2]
    c = multi_extreme_fibers(add, subtract=[])
    return i / c


def multi_principal_elast_sect_mod(add, subtract=[]):
    """
    Calculates the section modulii about the principal axes. Returns an array
    of shape (2,).

    Parameters
    ----------
    add : list
        A list of (x, y) boundary coordinates for shapes included in the
        cross section. Each set of boundary coordinates should be of the
        shape (N, 2).
    subtract : list
        A list of (x, y) boundary coordinates for cut out shapes to be
        subtracted from the cross section. Each set of boundary coordinates
        should be of the shape (N, 2).
    """
    i = multi_principal_inertias(add, subtract)
    c = multi_principal_extreme_fibers(add, subtract)
    return i / c


def multi_plot_section(add, subtract=[], ax=None, title='', symbols={}):
    """
    Plots a cross section consisting of multiple shapes.

    Parameters
    ----------
    add : list
        A list of (x, y) boundary coordinates for shapes included in the
        cross section. Each set of boundary coordinates should be of the
        shape (N, 2).
    subtract : list
        A list of (x, y) boundary coordinates for cut out shapes to be
        subtracted from the cross section. Each set of boundary coordinates
        should be of the shape (N, 2).
    ax : :class:`matplotlib.axes.Axes`
        The axes to which the plot will be added. If None, a new figure
        and axes will be created.
    title : str
        The title of the figure.
    symbols : dict
        A dictionary of symbols to use for the plot. Valid keys are:

        * `add`: The boundary lines for included shapes, default is 'b-'.
        * `subtract`: The boundary lines for subtracted shapes, default is 'r-'
        * `centroid`: The centroid point, default is 'r+'.
        * `primary_axes`: The primary axes lines, default is 'g-.'
        * `principal_axes`: The pricipal axes lines, default is 'm-.'
    """
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111,
            title=title,
            xlabel='X',
            ylabel='Y',
            aspect='equal'
        )

    sym = dict(
        add='b-',
        subtract='r-',
        centroid='',
        primary_axes='g-.',
        principal_axes='m-.'
    )
    sym.update(symbols)

    # Plot boundary
    for x in add:
        x = close_points(x)
        ax.plot(x[:,0], x[:,1], sym['add'])

    for x in subtract:
        x = close_points(x)
        ax.plot(x[:,0], x[:,1], sym['subtract'])

    # Plot centroid
    o = multi_centroid(add, subtract)
    if sym['centroid'] not in {'', None}:
        ax.plot(o[0], o[1], sym['centroid'])

    # Plot axes
    ang = multi_principal_angles(add, subtract)
    c = [multi_extreme_fibers(add, subtract),
         multi_principal_extreme_fibers(add, subtract)]
    c = 1.25 * max(map(np.max, c))

    if sym['primary_axes'] not in {'', None}:
        x = np.array([o + (0, -c), o + (0, c)])
        ax.plot(x[:,0], x[:,1], sym['primary_axes'])

        x = np.array([o + (-c, 0), o + (c, 0)])
        ax.plot(x[:,0], x[:,1], sym['primary_axes'])

    if sym['principal_axes'] not in {'', None} and np.min(np.abs(ang)) >= TOL:
        du, dv = c * np.column_stack([np.cos(ang), np.sin(ang)])

        x = np.array([o - du, o + du])
        ax.plot(x[:,0], x[:,1], sym['principal_axes'])

        x = np.array([o - dv, o + dv])
        ax.plot(x[:,0], x[:,1], sym['principal_axes'])

    return ax


def multi_section_summary(add, subtract=[]):
    """
    Returns a dictionary with a summary of cross sectional properties
    for the composite shape.

    Parameters
    ----------
    add : list
        A list of (x, y) boundary coordinates for shapes included in the
        cross section. Each set of boundary coordinates should be of the
        shape (N, 2).
    subtract : list
        A list of (x, y) boundary coordinates for cut out shapes to be
        subtracted from the cross section. Each set of boundary coordinates
        should be of the shape (N, 2).

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
    add = [close_points(x) for x in add]
    subtract = [close_points(x) for x in subtract]

    a = multi_area(add, subtract)
    x, y = multi_centroid(add, subtract)
    w, h = multi_dimensions(add)
    ix, iy, ij, ixy = multi_inertias(add, subtract)
    iz = np.min(multi_principal_inertias(add, subtract))
    rx, ry = multi_gyradii(add, subtract)
    rz = np.min(multi_principal_gyradii(add, subtract))
    sx, sy = multi_elast_sect_mod(add, subtract)
    sz = np.min(multi_principal_elast_sect_mod(add, subtract))

    summary = dict(
        area=a, x=x, y=y, width=w, height=h,
        inertia_x=ix, inertia_y=iy, inertia_j=ij, inertia_xy=ixy, inertia_z=iz,
        gyradius_x=rx, gyradius_y=ry, gyradius_z=rz,
        elast_sect_mod_x=sx, elast_sect_mod_y=sy, elast_sect_mod_z=sz
    )

    return summary
