import pytest
import numpy as np
from .polygon import *


def test_polygon_summary():
    # Inscribed
    p = polygon_summary(6, 1, is_inscribed=True)
    assert pytest.approx(p['area']) == 2.5980762113533

    p = polygon_summary(6, 1, 0.1, is_inscribed=True)
    a = 2.5980762113533 - 2.0327172275047
    assert pytest.approx(p['area']) == a

    # Circumscribed
    p = polygon_summary(6, 1, is_inscribed=False)
    assert pytest.approx(p['area']) == 3.4641016151378

    p = polygon_summary(6, 1, 0.1, is_inscribed=False)
    a = 3.4641016151378 - 2.8059223082616
    assert pytest.approx(p['area']) == a
