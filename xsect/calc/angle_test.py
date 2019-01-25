from __future__ import division
import pytest
from ..data import query_aisc
from .angle import *


def test_angle_points():
    angle_points(8, 8, 1.125)


def test_angle_summary():
    a = angle_summary(8, 8, 1.125)
    b = query_aisc('L8x8x1-1/8', version='15.0')
    del (a['elast_sect_mod_z'], a['inertia_xy'], a['inertia_j'],
         a['width'], a['height'])

    for k, x in a.items():
        assert pytest.approx(x, 0.01) == b[k]
