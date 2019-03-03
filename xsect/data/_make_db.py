import re
import pandas as pd
from config_db import DB_CONNECTION

__all__ = []


OPTIONS = dict(
    if_exists='replace',
    index=False
)


def gsheet_csv_url(url):
    """
    Returns the url for the Google Sheet csv export.

    Parameters
    ----------
    url : str
        The editor url string as found when viewing the sheet in a browser.
    """
    def get_sheet():
        for i, x in enumerate(s):
            if x == 'gid':
                return s[i+1]

        raise ValueError('Sheet ID not found in url {}'.format(url))

    s = re.split('/|#|=|&', url)

    key = s[5]
    sheet = get_sheet()

    return 'https://docs.google.com/spreadsheets/d/{}/export?gid={}&format=csv'.format(key, sheet)


def make_unique_columns(df):
    """
    Renames the data frame columns to be unique when exported to an SQL
    database.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The data frame.
    """
    names = {}
    lnames = set()

    for x in list(df):
        n = x

        # Get a unique name
        while n.lower() in lnames:
            n = n + '_'

        lnames.add(n.lower())
        names[x] = n

    df.rename(columns=names, inplace=True)

    return df


def rename_columns_15_0(df):
    """
    Renames the version 15.0 data frame columns.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The data frame.
    """
    names = {
        'AISC_Manual_Label': 'name',
        'W': 'unit_weight',
        'A': 'area',
        'Ix': 'inertia_x',
        'Iy': 'inertia_y',
        'Iz': 'inertia_z',
        'Zx': 'plast_sect_mod_x',
        'Zy': 'plast_sect_mod_y',
        'Sx': 'elast_sect_mod_x',
        'Sy': 'elast_sect_mod_y',
        'Sz': 'elast_sect_mod_z',
        'rx': 'gyradius_x',
        'ry': 'gyradius_y',
        'rz': 'gyradius_z',
        'J': 'inertia_t',
    }

    df.rename(columns=names, inplace=True)

    return df


def write_aisc_metric_15_0():
    """
    Writes the 'aisc_metric_15_0' table to the database.
    """
    url = 'https://docs.google.com/spreadsheets/d/1RwpcQxKsQmb_ylxR5Zx4JYWf9_A4Cd-6KrUrXt3ynls/edit#gid=55672305'
    table = 'aisc_metric_15_0'

    url = gsheet_csv_url(url)

    df = pd.read_csv(url)
    rename_columns_15_0(df)
    make_unique_columns(df)

    df.to_sql(table, DB_CONNECTION, **OPTIONS)


def write_aisc_imperial_15_0():
    """
    Writes the 'aisc_imperial_15_0' table to the database.
    """
    url = 'https://docs.google.com/spreadsheets/d/1RwpcQxKsQmb_ylxR5Zx4JYWf9_A4Cd-6KrUrXt3ynls/edit#gid=1797343786'
    table = 'aisc_imperial_15_0'

    url = gsheet_csv_url(url)

    df = pd.read_csv(url)
    rename_columns_15_0(df)
    make_unique_columns(df)

    df.to_sql(table, DB_CONNECTION, **OPTIONS)


def write_database():
    """
    Writes all data to the database.
    """
    write_aisc_metric_15_0()
    write_aisc_imperial_15_0()


if __name__ == '__main__':
    write_database()
