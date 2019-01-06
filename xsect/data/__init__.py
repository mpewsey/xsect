"""
========================
Data (:mod:`xsect.data`)
========================

The data submodule contains functions used for acquiring data from the
package database.

Database Sources
================
The properties contained in the SQLite database are acquired from the following
sources:

AISC Shapes
-----------
The database includes steel shapes from the American Institute of Steel
Construction (AISC), which were taken from the below publicly available
locations. For variable descriptions, please consult the README included
with their data.

* `AISC Shapes Database v15.0 <https://www.aisc.org/globalassets/aisc/manual/v15.0-shapes-database/aisc-shapes-database-v15.0.xlsx>`_


Database Query Functions
========================
Contains methods for accessing AISC shape information from the database.

.. autosummary::
    :toctree: generated/

    filter_aisc
    query_aisc
    query_aisc_shapes


Building the Database
=====================
Developers adding or modifying data in the database should modify the
`_make_db.py` file in the data submodule. Files on which this script depend
should be placed in the data folder but not be included in any package
distributions.

During development, this script may be run to rebuild the database completely
from scratch by running the following command from the root directory:

.. code-block:: none

    python xsect/data/_make_db.py


The database itself should be included with all package distributions
such that the end user does not need to build the database themselves.
"""

from .query_db import *
