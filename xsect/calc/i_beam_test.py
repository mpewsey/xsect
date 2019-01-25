from __future__ import division
import pytest
from ..data import query_aisc
from .i_beam import *


def test_i_beam_points():
    i_beam_points(44, 15.9, 1.77, 1.03)


def test_i_beam_summary():
    a = i_beam_summary(44, 15.9, 1.77, 1.03)
    b = query_aisc('W44X335', version='15.0')
    del (a['elast_sect_mod_z'], a['inertia_xy'], a['inertia_j'], a['x'], a['y'],
         a['inertia_z'], a['gyradius_z'], a['width'], a['height'])

    for k, x in a.items():
        assert pytest.approx(x, 0.01) == b[k]
