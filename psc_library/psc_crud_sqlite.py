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
import psc_logging as psc_logs

class connectSQLite:
    def __init__(self, database):
        self.conn = None
        try:
            self.conn = sql.connect(database)
            psc_logs.logger.info(sql.version)
        
            self.cur = self.conn.cursor()
            psc_logs.logger.info(f"Connected to SQLite database '{database}'.")
        except:
            psc_logs.logger.exception("")
    
    def create_table(self, table_name, create_query):
        try:
            self.conn.execute(create_query)
        except Exception as e: # catch *all* exceptions
            psc_logs.logger.debug(f"Error creating table {table_name}: {e}")
        else:
            self.conn.commit()
            psc_logs.logger.debug(f"Table '{table_name}' created successfully.")

    def close_conn(self):
        self.conn.close()
        psc_logs.logger.info("Connection to SQLite database closed.")

    #CRUD - CREATE - READ - UPDATE - DELETE
    #Create
    def insert_record(self, table, attributes, values):
        try:
            pass
        except Exception as e: # catch *all* exceptions
            psc_logs.logger.debug(f"Error inserting record: {e}")
        else:
            pass

    def insert_records(self, data):
        try:
            pass
        except Exception as e: # catch *all* exceptions
            psc_logs.logger.debug(f"Error inserting records: {e}")
        else:
            pass

    #Read
    def select_records(self, table, limit=10):
        psc_logs.logger.debug("Processing select")
        psc_logs.logger.debug(f"SELECT TOP {limit} * FROM {table}")
        return self.cur.execute(f"SELECT TOP {limit} * FROM {table}").fetchall()

    def select_record(self, table, attribute, value):
        psc_logs.logger.debug("Processing select with key")
        psc_logs.logger.debug(f"SELECT * FROM {table} WHERE {attribute} = '{value}'")
        return self.cur.execute(f"SELECT * FROM {table} WHERE {attribute} = '{value}'").fetchone()

    #Update
    def update_record(self, table, key_attribute, key_value, attribute, value, free_where=''):
        try:
            pass
        except Exception as e: # catch *all* exceptions
            psc_logs.logger.debug(f"Error updating record: {e}")
        else:
            pass

    #Delete
    def delete_record(self, table, attribute, value):
        try:
            pass
        except Exception as e: # catch *all* exceptions
            psc_logs.logger.debug(f"Error deleting record: {e}")
        else:
            pass

    #Free SQL Query
    def free_query(self, query):
        try:
            psc_logs.logger.debug(f"Executing query: {query}")
            self.cur.execute(query).fetchall()
        except Exception as e: # catch *all* exceptions
            psc_logs.logger.debug(f"Error executing query: {e}")
        else:
            self.conn.commit()
            psc_logs.logger.debug(f"Query executed successfully.")
