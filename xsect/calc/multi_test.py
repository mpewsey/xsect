from __future__ import division
import numpy as np
from pytest import approx
from .cruciform import cruciform_points
from .multi import *


def sample_cruciform(rand):
    args = [(8, 8, 1.125, 1.125, 0.5), (8, 6, 1, 1, 0.5), (6, 8, 1, 1, 0.5),
            (8, 4, 5/8, 5/8, 0.5), (4, 8, 5/8, 5/8, 0.5), (2, 2, 0.125, 0.125, 0.5)]

    p1 = [cruciform_points(*x) for x in args]
    p2 = [[z + y for z in x] for x, y in zip(p1, rand)]
    return p1 + p2


def test_multi_area():
    np.random.seed(9308409)
    rand = np.random.uniform(-1000, 1000, (6, 2))

    a = 4 * np.array([16.7, 13, 13, 7.11, 7.11, 0.484] * 2)

    points = sample_cruciform(rand)
    sol = np.array([multi_area(x) for x in points])
    assert approx(sol, 0.01) == a


def test_multi_centroid():
    np.random.seed(53810274)
    rand = np.random.uniform(-1000, 1000, (6, 2))

    c = np.zeros((6, 2))
    c = np.concatenate([c, rand])

    points = sample_cruciform(rand)
    sol = np.array([multi_centroid(x) for x in points])
    assert approx(sol.ravel(), 0.01) == c.ravel()


def test_multi_plot_section():
    rect = np.array([(0, 0), (330, 0), (330, 280), (0, 280), (0, 0)])
    tri = np.array([(0, 0), (210, 0), (0, 210), (0, 0)]) + (50, 40)

    multi_plot_section(add=[rect], subtract=[tri], symbols=dict(centroid='r+'))
