# This module configures matplotlib

import os
import matplotlib

if 'DISPLAY' not in os.environ:
    matplotlib.use('Agg')

import matplotlib.pyplot as plt

__all__ = ['plt']
