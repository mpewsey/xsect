from __future__ import division
import pytest
from .cross_section import CrossSection
from .cruciform import cruciform_points


def test_repr():
    # Passes if repr doesn't raise exception
    xsect = CrossSection('Test', area=1.0)
    repr(xsect)


def test_from_points():
    add = cruciform_points(8, 8, 1.125)
    CrossSection.from_points('4L8x8x1.125', add)


def test_from_aisc_latest():
    # Latest version, Imperial
    xsect = CrossSection.from_aisc('L8x8x1-1/8', metric=False, version=None)
    del xsect.width, xsect.height

    for x in vars(xsect).values():
        assert x is not None

    assert len(xsect.meta) > 0

    # Latest version, Metric
    xsect = CrossSection.from_aisc('L305X305X34.9', metric=True, version=None)
    del xsect.width, xsect.height

    for x in vars(xsect).values():
        assert x is not None

    assert len(xsect.meta) > 0

    # Latest version, No Meta
    xsect = CrossSection.from_aisc('L305X305X34.9', metric=True, version=None, include_meta=False)
    del xsect.width, xsect.height

    for x in vars(xsect).values():
        assert x is not None

    assert len(xsect.meta) == 0

    # Round
    xsect = CrossSection.from_aisc('Pipe26STD', metric=False, version='15.0')
    assert hasattr(xsect, 'is_round')


def test_from_aisc_v15_0():
    # Version 15.0, Imperial
    xsect = CrossSection.from_aisc('L8x8x1-1/8', metric=False, version='15.0')
    del xsect.width, xsect.height

    for x in vars(xsect).values():
        assert x is not None

    assert len(xsect.meta) > 0

    # Version 15.0, Metric
    xsect = CrossSection.from_aisc('L305X305X34.9', metric=True, version='15.0')
    del xsect.width, xsect.height

    for x in vars(xsect).values():
        assert x is not None

    assert len(xsect.meta) > 0

    # Round
    xsect = CrossSection.from_aisc('Pipe26STD', metric=False, version='15.0')
    assert hasattr(xsect, 'is_round')
