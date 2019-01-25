from __future__ import division
import pytest
from ..data import query_aisc
from .cruciform import *


def test_cruciform_points():
    cruciform_points(12, 12, 1+3/8, separation=3/4)


def test_cruciform_summary():
    cruciform_summary(12, 12, 1+3/8, separation=3/4)
