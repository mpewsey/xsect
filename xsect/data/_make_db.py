import os
import sqlite3
import pandas as pd

DATA_FOLDER = os.path.abspath(os.path.dirname(__file__))
SQLDB = os.path.join(DATA_FOLDER, 'xsect.sqlite')
DB_CONNECTION = sqlite3.connect(SQLDB)

__all__ = []


def write_table(excel_file, excel_tab, sql_table):
    """
    Writes the Excel table to the SQLite database.

    Parameters
    ----------
    excel_file : str
        Path to the Excel file.
    excel_tab : str
        The name of the tab in the Excel file to load.
    sql_table : str
        The name of the SQL table to write the data to.
    """
    options = dict(
        if_exists='replace',
        index=False
    )

    excel_file = os.path.join(DATA_FOLDER, excel_file)
    df = pd.read_excel(excel_file, excel_tab)
    df.to_sql(sql_table, DB_CONNECTION, **options)


def write_aisc_metric_15_0():
    """
    Writes the 'aisc_metric_15_0' table to the database.
    """
    path = 'aisc-shapes-database-v15.0.xlsx'
    tab = 'metric'
    table = 'aisc_metric_15_0'

    write_table(path, tab, table)


def write_aisc_imperial_15_0():
    """
    Writes the 'aisc_imperial_15_0' table to the database.
    """
    path = 'aisc-shapes-database-v15.0.xlsx'
    tab = 'imperial'
    table = 'aisc_imperial_15_0'

    write_table(path, tab, table)


def write_database():
    """
    Writes all data to the database.
    """
    write_aisc_metric_15_0()
    write_aisc_imperial_15_0()


if __name__ == '__main__':
    write_database()
