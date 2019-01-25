from __future__ import division
import pytest
from ..data import query_aisc
from .double_angle import *


def test_double_angle_points():
    double_angle_points(12, 12, 1+3/8, separation=3/4)


def test_double_angle_summary():
    a = double_angle_summary(12, 12, 1+3/8, separation=3/4)
    b = query_aisc('2L12X12X1-3/8X3/4', version='15.0')
    del (a['elast_sect_mod_z'], a['inertia_xy'], a['inertia_j'], a['x'],
         a['inertia_z'], a['gyradius_z'], a['width'], a['height'])

    for k, x in a.items():
        assert pytest.approx(x, 0.02) == b[k]
