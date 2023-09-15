# psc_crud_sqlite.py

"""
CRUD to manipulate SQLite database

@Author: Filipe Santos

"""

"""
TO DO
Connect
Initialize DB - Create DB - Create Table
Insert
Select
Update
Delete
"""

import sqlite3 as sql
import os
from psc_library.psc_logging import logger

class connectSQLite:
    def __init__(self, database):
        self.conn = None
        try:
            self.conn = sql.connect(database)
            logger.info(f"SQLite version {sql.version}.")
        
            self.cur = self.conn.cursor()
            logger.info(f"Connected to SQLite database '{database}'.")
        except Exception as e:
            logger.exception(f"Error connecting to database {database}: {e}")
    
    #Create table
    def create_table(self, table, create_query):
        try:
            self.conn.execute(create_query)
        except Exception as e: # catch *all* exceptions
            logger.exception(f"Error creating table {table}: {e}")
            self.conn.rollback()
        else:
            self.conn.commit()
            logger.debug(f"Table '{table}' created successfully.")

    #Drop table
    def drop_table(self, table):
        try:
            self.cur.execute(f"DROP table {table}")
        except Exception as e: # catch *all* exceptions
            logger.debug(f"Error deleting record: {e}")
        else:
            self.conn.commit()
            logger.debug(f"Table '{table}' deleted successfully.")

    #Close connection
    def close_conn(self):
        self.conn.close()
        logger.info("Connection to SQLite database closed.")

    #CRUD - CREATE - READ - UPDATE - DELETE
    #Create
    def insert_record(self, table, attributes, values):
        try:
            logger.debug("Processing insert:")
            logger.debug(f"INSERT INTO {table} {attributes} VALUES {values}")
            self.cur.execute(f"INSERT INTO {table} {attributes} VALUES {values}")
        except Exception as e:
            logger.debug(f"Error inserting record: {e}")
            self.conn.rollback()
            logger.debug("Operation reversed (rollback)")
        else:
            self.conn.commit()
            logger.debug("Record inserted successfully!")

    def insert_records(self, data):
        try:
            pass
        except Exception as e: # catch *all* exceptions
            logger.debug(f"Error inserting records: {e}")
        else:
            self.conn.commit()
            logger.debug("RecordS inserted successfully!")

    #Read
    def select_records(self, table, arguments="*", orderby=None, limit=10):
        logger.debug("Processing select:")
        if limit == None:
            top_limit = ""
        else:
            top_limit = f" TOP {limit}"
        if orderby == None:
            order_by = ""
        else:
            order_by = f"ORDER BY {orderby}"
        logger.debug(f"SELECT{top_limit} {arguments} FROM {table} {order_by}")
        return self.cur.execute(f"SELECT{top_limit} {arguments} FROM {table} {order_by}").fetchall()

    def select_record(self, table, attribute, value):
        logger.debug("Processing select with key:")
        logger.debug(f"SELECT * FROM {table} WHERE {attribute} = '{value}'")
        return self.cur.execute(f"SELECT * FROM {table} WHERE {attribute} = '{value}'").fetchone()

    #Update
    def update_record(self, table, key_attribute, key_value, attribute, value, free_where=''):
        try:
            pass
        except Exception as e: # catch *all* exceptions
            logger.debug(f"Error updating record: {e}")
        else:
            pass

    #Delete
    def delete_record(self, table, attribute, value):
        try:
            pass
        except Exception as e: # catch *all* exceptions
            logger.debug(f"Error deleting record: {e}")
        else:
            pass

    #Free SQL Query
    def free_query(self, query):
        try:
            logger.debug(f"Executing free query:")
            logger.debug(query)
            return self.cur.execute(query).fetchall()
        except Exception as e: # catch *all* exceptions
            logger.debug(f"Error executing query: {e}")
        else:
            self.conn.commit()
            logger.debug(f"Query executed successfully.")


def check_database(database):
    ''' Check if the database exists or not '''
    validSQLconnection = False
    try:
        print(f'Checking if {database.db_name} exists or not...')
        database.conn = sql.connect(database)
        logger.debug(f'Database exists. Succesfully connected to {database.db_name}')
        validSQLconnection = True
        return validSQLconnection
        
    except sql.OperationalError as err:
        logger.debug(f'Database {database.db_name} does not exist.')

