# This module configures matplotlib

import os
import sys
import matplotlib

if sys.version_info[0] < 3 and 'DISPLAY' not in os.environ:
    matplotlib.use('Agg')

__all__ = []
