"""
==============================================
Cross Section Calculations (:mod:`xsect.calc`)
==============================================

Contains functions and classes for calculating and storing cross sectional
properties for structural members.


Cross Section Classes
=====================
The below class provides a container for storing cross sectional properties.

.. autosummary::
    :toctree: generated/

    CrossSection


Boundary Functions
==================
The following functions may be used to calculate cross sectional properties
based on sections defined by boundary points.

.. plot:: ../examples/boundary_ex1.py

.. autosummary::
    :toctree: generated/

    rotate2
    close_points
    area
    centroid
    inertias
    principal_inertias
    principal_angles
    gyradii
    principal_gyradii
    extreme_fibers
    principal_extreme_fibers
    elast_sect_mod
    principal_elast_sect_mod
    plot_section
    section_summary


Multi-Boundary Functions
========================
The following functions may be used to calculate cross sectional properties
for composite sections composed of multiple elements which are defined
by boundary points.

.. plot:: ../examples/multi_section_ex1.py

.. autosummary::
    :toctree: generated/

    multi_area
    multi_centroid
    multi_inertias
    multi_principal_inertias
    multi_principal_angles
    multi_gyradii
    multi_principal_gyradii
    multi_extreme_fibers
    multi_principal_extreme_fibers
    multi_elast_sect_mod
    multi_principal_elast_sect_mod
    multi_plot_section
    multi_section_summary


Round Functions
===============
The following functions may be used to calculate cross sectional properties
for round sections, such as rounds and pipes.

.. plot:: ../examples/round_ex1.py

.. autosummary::
    :toctree: generated/

    round_area
    round_inertia
    round_gyradius
    round_sect_mod
    round_points
    round_summary


Polygon Functions
=================
The following functions may be used to calculate the cross sectional properties
for solid or thin walled polygon sections.

.. plot:: ../examples/polygon_ex1.py

.. autosummary::
    :toctree: generated/

    polygon_points
    polygon_summary


Angle Functions
===============
The following functions may be used to calculate cross sectional properties
for angle or "L" shape sections.

.. plot:: ../examples/angle_ex1.py

.. autosummary::
    :toctree: generated/

    angle_points
    angle_summary


Double Angle Functions
======================
The following functions may be used to calculate cross sectional properties
for double angle or "2L" shape sections.

.. plot:: ../examples/double_angle_ex1.py

.. autosummary::
    :toctree: generated/

    double_angle_points
    double_angle_summary


Cruciform Functions
===================
The following functions may be used to calculate cross sectional properties
for cruciform or "4L" shape sections.

.. plot:: ../examples/cruciform_ex1.py

.. autosummary::
    :toctree: generated/

    cruciform_points
    cruciform_summary


I-Beam Functions
================
The following functions may be used to calculate cross sectional properties
for I-beam sections.

.. plot:: ../examples/i_beam_ex1.py

.. autosummary::
    :toctree: generated/

    i_beam_points
    i_beam_summary


T-Beam Functions
================
The following functions may be used to calculate cross sectional properties
for T-beam sections.

.. plot:: ../examples/t_beam_ex1.py

.. autosummary::
    :toctree: generated/

    t_beam_points
    t_beam_summary
"""

from .angle import *
from .boundary import *
from .cross_section import *
from .cruciform import *
from .double_angle import *
from .i_beam import *
from .multi import *
from .polygon import *
from .round import *
from .t_beam import *
