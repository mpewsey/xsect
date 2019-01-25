from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

__all__ = [
    'rotate2',
    'close_points',
    'dimensions',
    'area',
    'centroid',
    'inertias',
    'principal_inertias',
    'principal_angles',
    'gyradii',
    'principal_gyradii',
    'extreme_fibers',
    'principal_extreme_fibers',
    'elast_sect_mod',
    'principal_elast_sect_mod',
    'plot_section',
    'section_summary'
]

TOL = 1e-8 # Tolerance for principal angles


def rotate2(x, angle, origin=(0, 0)):
    """
    Rotates an array of 2D row vectors by an angle about the specified origin.
    Returns an array of shape (N, 2).

    Parameters
    ----------
    x : array
        An array of (x, y) vectors or shape (N, 2).
    angles : float
        Counterclockwise angle from the x-axis in radians.
    origin : array
        The origin about which to rotate the vectors.
    """
    o = np.asarray(origin)
    x = np.asarray(x)
    x = x - o

    c, s = np.cos(angle), np.sin(angle)
    r = np.array([[c, -s], [s, c]])

    x = np.array([np.dot(r, v) for v in x])

    return x + o


def close_points(points):
    """
    If the input points do not form a closed polygon, closes the polygon
    and returns the result.

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
    """
    p = np.asarray(points)
    if (p[0] == p[-1]).all():
        return p
    return np.append(p, [p[0]], axis=0)


def dimensions(points):
    """
    Returns the width and height of the section defined by the input boundary
    points.

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
    """
    p = np.asarray(points)
    mn, mx = np.min(p, axis=0), np.max(p, axis=0)
    return mx - mn


def area(points):
    """
    Returns the area enclosed by the input points.

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
    """
    p = close_points(points)
    x, y = p[:,0], p[:,1]
    a = 0.5 * np.sum(x[:-1]*y[1:] - x[1:]*y[:-1])
    return abs(a)


def centroid(points):
    """
    Returns the (x, y) centroid coordinates for the shape defined by the
    input boundary points. The result is an array of shape (2,).

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
    """
    p = close_points(points)

    x, y = p[:,0], p[:,1]
    a = 3 * np.sum(x[:-1]*y[1:] - x[1:]*y[:-1])

    c = x[:-1] * y[1:] - x[1:] * y[:-1]
    cx = (x[:-1] + x[1:]) * c
    cx = np.sum(cx) / a

    cy = (y[:-1] + y[1:]) * c
    cy = np.sum(cy) / a

    return np.array([cx, cy])


def inertias(points, origin=None):
    """
    Returns the area moment of inertias for the shape defined by the
    input boundary points. The result is an array of shape (4,).

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
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
        origin = centroid(points)

    p = close_points(points) - origin
    x, y = p[:,0], p[:,1]

    c = x[:-1] * y[1:] - x[1:] * y[:-1]
    ix = c * (y[:-1]**2 + y[:-1]*y[1:] + y[1:]**2)
    ix = np.sum(ix) / 12

    iy = c * (x[:-1]**2 + x[:-1]*x[1:] + x[1:]**2)
    iy = np.sum(iy) / 12

    ixy = c * (x[:-1]*y[1:] + 2*x[:-1]*y[:-1] + 2*x[1:]*y[1:] + x[1:]*y[:-1])
    ixy = np.sum(ixy) / 24

    if ix < 0: ixy = -ixy
    ix, iy = abs(ix), abs(iy)
    ij = ix + iy

    return np.array([ix, iy, ij, ixy])


def principal_inertias(points):
    """
    Returns the area moment of inertias about the principal axes. The result
    is an array of shape (2,).

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
    """
    ix, iy, ij, ixy = inertias(points)
    avg = 0.5*ij
    diff = 0.5*(ix - iy)
    diff = (diff**2 + ixy**2)**0.5
    iu, iv = avg + diff, avg - diff
    return np.array([iu, iv])


def principal_angles(points):
    """
    Returns the principal angles. The result is an array of shape (2,).

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
    """
    ix, iy, _, ixy = inertias(points)
    diff = ix - iy

    if abs(ixy) < TOL and abs(diff) < TOL:
        alpha = 0
    else:
        alpha = 0.5*np.arctan2(-ixy, 0.5*diff)

    beta = alpha + np.pi/2
    return np.array([alpha, beta])


def gyradii(points):
    """
    Returns the radii of gyration about the x and y axes. The result is an
    array of shape (2,).

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
    """
    i = inertias(points)[:2]
    a = area(points)
    return np.sqrt(i / a)


def principal_gyradii(points):
    """
    Returns the radii of gyration about the principal axes. The result is
    an array of shape (2,).

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
    """
    points = close_points(points)
    i = principal_inertias(points)
    a = area(points)
    return np.sqrt(i / a)


def extreme_fibers(points):
    """
    Returns the extreme fibers from the x and y axes. The result is an array
    of shape (2,).

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
    """
    points = np.asarray(points) - centroid(points)
    c = np.max(np.abs(points), axis=0)
    return np.flip(c, axis=0)


def principal_extreme_fibers(points):
    """
    The returns the extreme fibers from the principal axes. The result is
    an array of shape (2,).

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
    """
    points = np.asarray(points) - centroid(points)
    alpha, _ = principal_angles(points)
    c = rotate2(points, alpha)
    c = np.max(np.abs(points), axis=0)
    return np.flip(c, axis=0)


def elast_sect_mod(points):
    """
    Returns the section modulii about the x and y axes. The result is an
    array of shape (2,).

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
    """
    i = inertias(points)[:2]
    c = extreme_fibers(points)
    return i / c


def principal_elast_sect_mod(points):
    """
    Returns the section modulii about the principal axes. The result is an
    array of shape (2,).

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
    """
    i = principal_inertias(points)[:2]
    c = principal_extreme_fibers(points)
    return i / c


def plot_section(points, ax=None, title='', symbols={}):
    """
    Plots the cross section defined by the input boundary points.

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).
    ax : :class:`matplotlib.axes.Axes`
        The axes to which the plot will be added. If None, a new figure
        and axes will be created.
    title : str
        The title of the figure.
    symbols : dict
        A dictionary of symbols to use for the plot. Valid keys are:

        * `boundary`: The boundary lines, default is 'b-'.
        * `centroid`: The centroid point, default is ''.
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
        boundary='b-',
        centroid='',
        primary_axes='g-.',
        principal_axes='m-.'
    )
    sym.update(symbols)

    # Plot boundary
    p = close_points(points)
    ax.plot(p[:,0], p[:,1], sym['boundary'])

    # Plot centroid
    o = centroid(p)
    if sym['centroid'] not in {'', None}:
        ax.plot(o[0], o[1], sym['centroid'])

    # Plot axes
    ang = principal_angles(p)
    c = [extreme_fibers(p), principal_extreme_fibers(p)]
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


def section_summary(points):
    """
    Returns a dictionary with a summary of cross sectional properties
    for the shape defined by the input boundary points.

    Parameters
    ----------
    points : array
        An array of (x, y) coordinates of shape (N, 2).

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
    p = close_points(points)

    a = area(p)
    x, y = centroid(p)
    w, h = dimensions(p)

    ix, iy, ij, ixy = inertias(p)
    iz = np.min(principal_inertias(p))

    rx, ry = gyradii(p)
    rz = np.min(principal_gyradii(p))

    sx, sy = elast_sect_mod(p)
    sz = np.min(principal_elast_sect_mod(p))

    summary = dict(
        area=a, x=x, y=y, width=w, height=h,
        inertia_x=ix, inertia_y=iy, inertia_j=ij, inertia_xy=ixy, inertia_z=iz,
        gyradius_x=rx, gyradius_y=ry, gyradius_z=rz,
        elast_sect_mod_x=sx, elast_sect_mod_y=sy, elast_sect_mod_z=sz
    )

    return summary
