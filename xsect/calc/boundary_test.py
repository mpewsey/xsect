from __future__ import division
import numpy as np
from pytest import approx
from .boundary import *
from .angle import angle_points


def sample_angles(rand):
    args = [(8, 8, 1.125), (8, 6, 1), (6, 8, 1),
            (8, 4, 5/8), (4, 8, 5/8), (2, 2, 0.125)]

    p1 = [angle_points(*x) for x in args]
    p2 = [x * (-1, 1) for x in p1]
    p3 = [x * (1, -1) for x in p1]
    p4 = [x * (-1, -1) for x in p1]
    p5 = [x + y for x, y in zip(p1, rand)]
    p6 = [x + y for x, y in zip(p2, rand)]
    p7 = [x + y for x, y in zip(p3, rand)]
    p8 = [x + y for x, y in zip(p4, rand)]

    return p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8


def test_dimensions():
    np.random.seed(3894731)
    rand = np.random.uniform(-1000, 1000, (6, 2))

    points = sample_angles(rand)
    sol = np.array([dimensions(x) for x in points])
    x = np.array([8, 6, 8, 4, 8, 2] * 8)
    y = np.array([8, 8, 6, 8, 4, 2] * 8)

    assert approx(sol[:,0], 0.01) == x
    assert approx(sol[:,1], 0.01) == y


def test_close_points():
    x = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    y = close_points(x)

    x.append(x[0])
    x = np.array(x)

    assert approx(x) == y


def test_area():
    np.random.seed(2983432)
    rand = np.random.uniform(-1000, 1000, (6, 2))

    a = np.array([16.7, 13, 13, 7.11, 7.11, 0.484] * 8)

    points = sample_angles(rand)
    sol = np.array([area(x) for x in points])

    assert approx(sol, 0.01) == a


def test_centroid():
    np.random.seed(98908343)
    rand = np.random.uniform(-1000, 1000, (6, 2))

    c1 = np.array([(2.4, 2.4), (1.65, 2.65), (2.65, 1.65),
                   (0.902, 2.89), (2.89, 0.902), (0.534, 0.534)])
    c2 = c1 * (-1, 1)
    c3 = c1 * (1, -1)
    c4 = c1 * (-1, -1)
    c5 = c1 + rand
    c6 = c2 + rand
    c7 = c3 + rand
    c8 = c4 + rand
    c = np.concatenate([c1, c2, c3, c4, c5, c6, c7, c8])

    points = sample_angles(rand)
    sol = np.array([centroid(x) for x in points])

    assert approx(sol.ravel(), 0.025) == c.ravel()


def test_inertias():
    np.random.seed(89734323)
    rand = np.random.uniform(-1000, 1000, (6, 2))

    ix = np.array([98.1, 80.9, 38.8, 47, 8.11, 0.189] * 8)
    iy = np.array([98.1, 38.8, 80.9, 8.11, 47, 0.189] * 8)

    points = sample_angles(rand)
    sol = np.array([inertias(x) for x in points])

    assert approx(sol[:,0], 0.01) == ix
    assert approx(sol[:,1], 0.01) == iy


def test_principal_angles():
    np.random.seed(53243298)
    rand = np.random.uniform(-1000, 1000, (6, 2))

    ang = np.array([1.00, 0.542, np.tan(np.pi/2 - np.arctan(0.542)),
                    0.262, np.tan(np.pi/2 - np.arctan(0.262)), 1.00] * 8)

    points = sample_angles(rand)
    sol = np.array([principal_angles(x) for x in points])
    sol = np.abs(np.tan(np.min(sol, axis=1)))

    assert approx(sol, 0.01) == ang


def test_principal_inertias():
    np.random.seed(43893784)
    rand = np.random.uniform(-1000, 1000, (6, 2))

    iz = np.array([40.9, 21.3, 21.3, 5.24, 5.24, 0.0751] * 8)

    points = sample_angles(rand)
    sol = np.array([principal_inertias(x) for x in points])

    assert approx(np.min(sol, axis=1), 0.02) == iz


def test_gyradii():
    np.random.seed(619283539)
    rand = np.random.uniform(-1000, 1000, (6, 2))

    rx = np.array([2.41, 2.49, 1.72, 2.56, 1.06, 0.620] * 8)
    ry = np.array([2.41, 1.72, 2.49, 1.06, 2.56, 0.620] * 8)

    points = sample_angles(rand)
    sol = np.array([gyradii(x) for x in points])

    assert approx(sol[:,0], 0.01) == rx
    assert approx(sol[:,1], 0.01) == ry


def test_principal_gyradii():
    np.random.seed(72937493)
    rand = np.random.uniform(-1000, 1000, (6, 2))

    rz = np.array([1.56, 1.28, 1.28, 0.856, 0.856, 0.391] * 8)

    points = sample_angles(rand)
    sol = np.array([principal_gyradii(x) for x in points])

    assert approx(np.min(sol, axis=1), 0.02) == rz


def test_elast_sect_mod():
    np.random.seed(32934347)
    rand = np.random.uniform(-1000, 1000, (6, 2))

    sx = np.array([17.5, 15.1, 8.92, 9.2, 2.62, 0.129] * 8)
    sy = np.array([17.5, 8.92, 15.1, 2.62, 9.2, 0.129] * 8)

    points = sample_angles(rand)
    sol = np.array([elast_sect_mod(x) for x in points])

    assert approx(sol[:,0], 0.02) == sx
    assert approx(sol[:,1], 0.02) == sy


def test_principal_elast_sect_mod():
    p = [(0, 0), (3, 0), (3, 5), (0, 5), (0, 0)]
    a = principal_elast_sect_mod(p)

    sx = 3*5**2/6
    sy = 5*3**2/6
    b = np.array([sx, sy])

    assert approx(a, 0.01) == b


def test_plot_section():
    points = angle_points(8, 6, 1)
    plot_section(points, symbols=dict(centroid='r+'))


def test_section_summary():
    points = angle_points(8, 6, 1)
    section_summary(points)
