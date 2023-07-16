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
    
    def create_table(self, table_name, create_query):
        try:
            self.conn.execute(create_query)
        except Exception as e: # catch *all* exceptions
            logger.exception(f"Error creating table {table_name}: {e}")
            self.conn.rollback()
        else:
            self.conn.commit()
            logger.debug(f"Table '{table_name}' created successfully.")

    def close_conn(self):
        self.conn.close()
        logger.info("Connection to SQLite database closed.")

    #CRUD - CREATE - READ - UPDATE - DELETE
    #Create
    def insert_record(self, table, attributes, values):
        try:
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
    def select_records(self, table, limit=10):
        logger.debug("Processing select")
        logger.debug(f"SELECT TOP {limit} * FROM {table}")
        return self.cur.execute(f"SELECT TOP {limit} * FROM {table}").fetchall()

    def select_record(self, table, attribute, value):
        logger.debug("Processing select with key")
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
            logger.debug(f"Executing query: {query}")
            self.cur.execute(query).fetchall()
        except Exception as e: # catch *all* exceptions
            logger.debug(f"Error executing query: {e}")
        else:
            self.conn.commit()
            logger.debug(f"Query executed successfully.")
