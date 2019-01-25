import pytest
from .query_db import *


def test_query_aisc():
    # Bad version
    with pytest.raises(KeyError):
        odict = query_aisc('L8x8x1-1/8', metric=False, version='bad_version')


def test_query_aisc_shapes():
    q = query_aisc_shapes()
    assert len(q) > 0

    r = query_aisc_shapes('L')
    assert len(r) > 0

    assert len(q) > len(r)


def test_filter_aisc():
    filter_aisc(["type='L'", 'area>28'], order=['area'], columns=['name', 'area'])
