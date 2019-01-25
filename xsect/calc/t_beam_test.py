from __future__ import division
import pytest
from ..data import query_aisc
from .t_beam import *


def test_t_beam_points():
    t_beam_points(22, 15.9, 1.77, 1.03)


def test_t_beam_summary():
    a = t_beam_summary(22, 15.9, 1.77, 1.03)
    b = query_aisc('WT22X167.5', version='15.0')
    a['y'] = 22 - a['y']

    del (a['elast_sect_mod_z'], a['inertia_xy'], a['inertia_j'], a['x'],
         a['inertia_z'], a['gyradius_z'], a['width'], a['height'])

    for k, x in a.items():
        assert pytest.approx(x, 0.01) == b[k]
