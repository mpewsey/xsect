from __future__ import division
import pytest
import numpy as np
from .round import *


def test_round_area():
    # No thickness
    assert pytest.approx(round_area(4), 0.01) == 4*np.pi

    # With thickness
    assert pytest.approx(round_area(4, 1), 0.01) == 3*np.pi


def test_round_inertia():
    # No thickness
    a = np.pi*2**4/4
    assert pytest.approx(round_inertia(4), 0.01) == a

    # With thickness
    a = np.pi*(2**4 - 1)/4
    assert pytest.approx(round_inertia(4, 1), 0.01) == a


def test_round_gyradius():
    # No thickness
    assert pytest.approx(round_gyradius(4), 0.01) == 1

    # With thickness
    a = (0.25 * (2**4 - 1) / (2**2 - 1))**0.5
    assert pytest.approx(round_gyradius(4, 1), 0.01) == a


def test_round_sect_mod():
    # No thickness
    a = np.pi*4**3/32
    assert pytest.approx(round_sect_mod(4), 0.01) == a

    # With thickness
    a = np.pi*(4**4 - 2**4)/(32*4)
    assert pytest.approx(round_sect_mod(4, 1), 0.01) == a


def test_round_points():
    # No thickness
    round_points(4)

    # With thickness
    round_points(4, 1)


def test_round_summary():
    # No thickness
    summary = round_summary(4)
    odict = dict(
        area=4*np.pi,
        width=2,
        height=2,
        inertia_x=np.pi*2**4/4,
        inertia_y=np.pi*2**4/4,
        inertia_j=np.pi*2**4/2,
        gyradius_x=1,
        gyradius_y=1,
        gyradius_z=1,
        elast_sect_mod_x=np.pi*4**3/32,
        elast_sect_mod_y=np.pi*4**3/32,
        elast_sect_mod_z=np.pi*4**3/32
    )

    for k, x in odict.items():
        assert pytest.approx(x, 0.01) == summary[k]


    # With thickness
    summary = round_summary(4, 1)
    odict = dict(
        area=3*np.pi,
        width=2,
        height=2,
        inertia_x=np.pi*(2**4 - 1)/4,
        inertia_y=np.pi*(2**4 - 1)/4,
        inertia_j=np.pi*(2**4 - 1)/2,
        gyradius_x=(0.25 * (2**4 - 1) / (2**2 - 1))**0.5,
        gyradius_y=(0.25 * (2**4 - 1) / (2**2 - 1))**0.5,
        gyradius_z=(0.25 * (2**4 - 1) / (2**2 - 1))**0.5,
        elast_sect_mod_x=np.pi*(4**4 - 2**4)/(32*4),
        elast_sect_mod_y=np.pi*(4**4 - 2**4)/(32*4),
        elast_sect_mod_z=np.pi*(4**4 - 2**4)/(32*4)
    )

    for k, x in odict.items():
        assert pytest.approx(x, 0.01) == summary[k]

    round_summary(4, 1, np.pi/2)
