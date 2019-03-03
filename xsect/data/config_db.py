import os
import sqlite3

__all__ = [
    'DATA_FOLDER',
    'SQLDB',
    'DB_CONNECTION'
]


DATA_FOLDER = os.path.abspath(os.path.dirname(__file__))
SQLDB = os.path.join(DATA_FOLDER, 'xsect.sqlite')
DB_CONNECTION = sqlite3.connect(SQLDB)
