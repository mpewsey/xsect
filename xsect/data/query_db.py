import re
import pandas as pd
from .config_db import DB_CONNECTION

__all__ = [
    'original_names',
    'query_aisc',
    'query_aisc_shapes',
    'filter_aisc',
]


def original_names(names):
    """
    Returns the original names.

    Parameters
    ----------
    names : list
        A list of string names.
    """
    if len(names) > 0 and isinstance(names[0], (list, tuple)):
        names = [x[0] for x in names]

    return [re.sub('_+$', '', x) for x in names]


def _aisc_table(metric, version):
    """
    Returns the name of the AISC table matching the criteria.

    Parameters
    ----------
    metric : bool
        If True, searches for the name in the metric shape database. Otherwise,
        searches for the name in the imperial shape database.
    version : {'15.0'}
        The version of the shape database to query. If None, the latest version
        will be used.
    """
    if version is None:
        # Use the latest version
        version = '15.0'

    # Return the name of the version table
    if version == '15.0':
        if metric:
            return 'aisc_metric_15_0'
        else:
            return 'aisc_imperial_15_0'

    else:
        raise ValueError('Version {!r} not found.'.format(version))


def query_aisc(name, metric=False, version=None):
    """
    Queries the AISC steel shape database and returns a dictionary of the
    result.

    Parameters
    ----------
    name : str
        The name of the member.
    metric : bool
        If True, searches for the name in the metric shape database. Otherwise,
        searches for the name in the imperial shape database.
    version : {'15.0'}
        The version of the shape database to query. If None, the latest version
        will be used.
    """
    name = name.upper()
    table = _aisc_table(metric, version)

    statement = "SELECT * FROM {} WHERE UPPER(name)='{}';".format(table, name)
    cursor = DB_CONNECTION.execute(statement)

    header = original_names(cursor.description)
    row = cursor.fetchone()

    if not row:
        raise ValueError('Shape {} not found.'.format(name))

    odict = {k: x for k, x in zip(header, row) if x is not None}

    return odict


def query_aisc_shapes(shape=None, metric=False, version=None):
    """
    Queries the AISC steel shape database and returns a list of the shape
    names in the specified shape category.

    Parameters
    ----------
    shape : str
        The shape for which names will be returned. If None, all shape names
        will be returned.
    metric : bool
        If True, searches for the name in the metric shape database. Otherwise,
        searches for the name in the imperial shape database.
    version : {'15.0'}
        The version of the shape database to query. If None, the latest version
        will be used.
    """
    table = _aisc_table(metric, version)

    if shape is None:
        statement = "SELECT name FROM {};".format(table)
    else:
        shape = shape.upper()
        statement = "SELECT name FROM {} WHERE UPPER(type)='{}';".format(table, shape)

    cursor = DB_CONNECTION.execute(statement)

    return cursor.fetchall()


def filter_aisc(conditions, order=[], columns=[], metric=False, version=None):
    """
    Returns a dataframe with the data for the specified AISC steel shape
    database query.

    Parameters
    ----------
    conditions : list
        A list of condition strings to apply to the query.
    order : list of str
        Column names for ordering data. If none specified, no ordering will
        be applied.
    columns : list of str
        Column names to include in result. If none specified, all will be
        returned.

    Examples
    --------
    >>> filter_aisc(["type='L'", 'area>28'], order=['area'], columns=['name', 'area'])
               name  area
    0  L12X12X1-1/4  28.4
    1  L12X12X1-3/8  31.1
    """
    table = _aisc_table(metric, version)

    where = ' AND '.join(conditions)
    order = 'ORDER BY {}'.format(', '.join(order)) if order else ''
    columns = ', '.join(columns) if columns else '*'

    statement = "SELECT {} FROM {} WHERE {} {};".format(columns, table, where, order)

    cursor = DB_CONNECTION.execute(statement)

    header = original_names(cursor.description)

    df = pd.DataFrame(cursor.fetchall(), columns=header)

    return df
