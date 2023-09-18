# test_crud.py

"""
test_crud - Tests for CRUD functions

@Author: Filipe Santos
"""

import sys
sys.path.append("..")
sys.path.append("..\\psc_library")
print(sys.path)
import pytest

import psc_library.psc_crud_msaccess as psc_access
import psc_library.psc_crud_sqlite as psc_sqlite

# Test MSAccess CRUD
dir(psc_access.connectMSAccess)

connDBAccess = psc_access.connectMSAccess("..\\external\\databases\\bd1.mdb", "MASTER")

print('Tabelas do banco:')
for table in connDBAccess.show_tables():
    print(table.table_name)

# Test SQLite CRUD
dir(psc_sqlite.connectSQLite)

connSQLite = psc_sqlite.connectSQLite("..\\external\\databases\\mt940.db")
