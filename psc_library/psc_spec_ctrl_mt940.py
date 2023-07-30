# psc_spec_ctrl_mt940.py

"""
Specification Control MT940

@Author: Filipe Santos
@LastUpdate: 2023-06-09

ler extratos MT940
identificar contas, sequencias, datas, saldos e os blocos do extrato
guardar em BD SQLite
- Contas
- Sequencias / Data receção / Data Saldo / Saldos Inicial/Final?
validar se já registou o extrato (possiveis duplicados) se sim, guarda em outra tabela para mais tarde comparar com a tabela principal

- ### MT940 Manager ###
- read MT940 from file
- write MT940 to file - with criteria Account / Sequence / Date - options recode account
- save MT940 to database - no duplicates - key Account + Statement Sequence
- list from database by account / statement sequence - with criteria Account / Sequence / Date

- for later validate MT940

"""

import os
from datetime import datetime
import psc_util as psc_util
from psc_crud_sqlite import connectSQLite
from psc_logging import logger

class ctrl_mt940:
    def __init__(self, arg2, arg3, arg4="", arg5=""):
        logger.debug(f"Processing option: '{arg2}'.")
        logger.debug(f"Database: '{arg3}'.")
        logger.debug(f"Data in/out: '{arg4}'.")
        logger.debug(f"Criteria: '{arg5}'.")
        
        sqlite_connection = connectSQLite(arg3)

        # table "Accounts" : "CREATE TABLE IF NOT EXISTS Accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, account TEXT NOT NULL, iban TEXT, laststatementdate TEXT NOT NULL, expected INT NOT NULL); CREATE UNIQUE INDEX accounts_account on accounts(account);"
        # id INTEGER PRIMARY KEY AUTOINCREMENT, 
        # account TEXT NOT NULL, 
        # iban TEXT, 
        # laststatementdate TEXT NOT NULL, 
        # expected INT NOT NULL
        table_accounts = ("account", "iban", "laststatementdate", "expected")
        # table "IntegratedFiles" : "CREATE TABLE IF NOT EXISTS IntegratedFiles (id INTEGER PRIMARY KEY AUTOINCREMENT, integratedfile TEXT NOT NULL, filename TEXT NOT NULL, filedate TEXT NOT NULL, totalstatements INT NOT NULL, integrationdate TEXT NOT NULL); CREATE UNIQUE INDEX IntegratedFiles_integratedfile on IntegratedFiles(integratedfile);"
        # id INTEGER PRIMARY KEY AUTOINCREMENT, 
        # integratedfile TEXT NOT NULL, 
        # filename TEXT NOT NULL, 
        # filedate TEXT NOT NULL, 
        # totalstatements INT NOT NULL, 
        # integrationdate TEXT NOT NULL
        table_integrated_files = ("integratedfile", "filename", "filedate", "totalstatements", "integrationdate")
        # table "Statements" : "CREATE TABLE IF NOT EXISTS Statements (id INTEGER PRIMARY KEY AUTOINCREMENT, format TEXT NOT NULL, statementid TEXT NOT NULL, account TEXT NOT NULL, statementcode TEXT NOT NULL, openingbalancedate TEXT NOT NULL, openingbalanceamount REAL NOT NULL, closingbalancedate TEXT NOT NULL, closingbalanceamount REAL NOT NULL, sequencecomplete TEXT NOT NULL, sequence TEXT NOT NULL, segment TEXT NOT NULL, statement TEXT, originalfile TEXT, FOREIGN KEY (account) REFERENCES Accounts (account), FOREIGN KEY (originalfile) REFERENCES IntegratedFiles (integratedfile));"
        # id INTEGER PRIMARY KEY AUTOINCREMENT, 
        # format TEXT NOT NULL, 
        # statementid TEXT NOT NULL, 
        # account TEXT NOT NULL, 
        # statementcode TEXT NOT NULL, 
        # openingbalancedate TEXT NOT NULL, 
        # openingbalanceamount REAL NOT NULL, 
        # closingbalancedate TEXT NOT NULL, 
        # closingbalanceamount REAL NOT NULL, 
        # sequencecomplete TEXT NOT NULL, 
        # sequence TEXT NOT NULL, 
        # segment TEXT NOT NULL, 
        # statement TEXT, 
        # originalfile TEXT
        table_statements = ("format", "statementid", "account", "statementcode", "openingbalancedate", "openingbalanceamount", "closingbalancedate", "closingbalanceamount", "sequencecomplete", "sequence", "segment", "originalfile")
        table_statements_dups = ("format", "statementid", "account", "statementcode", "openingbalancedate", "openingbalanceamount", "closingbalancedate", "closingbalanceamount", "sequencecomplete", "sequence", "segment", "originalfile")

        if arg2 == "INIT_DB": # Initialize Database - Create tables
            sqlite_connection.create_table("Accounts", "CREATE TABLE IF NOT EXISTS Accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, account TEXT NOT NULL, iban TEXT, laststatementdate TEXT NOT NULL, expected INT NOT NULL);")
            sqlite_connection.free_query("CREATE UNIQUE INDEX accounts_account on accounts(account);")
            sqlite_connection.create_table("IntegratedFiles", "CREATE TABLE IF NOT EXISTS IntegratedFiles (id INTEGER PRIMARY KEY AUTOINCREMENT, integratedfile TEXT NOT NULL, filename TEXT NOT NULL, filedate TEXT NOT NULL, totalstatements INT NOT NULL, integrationdate TEXT NOT NULL);")
            sqlite_connection.free_query("CREATE UNIQUE INDEX IntegratedFiles_integratedfile on IntegratedFiles(integratedfile);")
            sqlite_connection.create_table("Statements", "CREATE TABLE IF NOT EXISTS Statements (id INTEGER PRIMARY KEY AUTOINCREMENT, format TEXT NOT NULL, statementid TEXT NOT NULL, account TEXT NOT NULL, statementcode TEXT NOT NULL, openingbalancedate TEXT NOT NULL, openingbalanceamount REAL NOT NULL, closingbalancedate TEXT NOT NULL, closingbalanceamount REAL NOT NULL, sequencecomplete TEXT NOT NULL, sequence TEXT NOT NULL, segment TEXT NOT NULL, statement TEXT, originalfile TEXT, FOREIGN KEY (account) REFERENCES Accounts (account), FOREIGN KEY (originalfile) REFERENCES IntegratedFiles (integratedfile));")
            sqlite_connection.create_table("StatementsDups", "CREATE TABLE IF NOT EXISTS Statements (id INTEGER PRIMARY KEY AUTOINCREMENT, format TEXT NOT NULL, statementid TEXT NOT NULL, account TEXT NOT NULL, statementcode TEXT NOT NULL, openingbalancedate TEXT NOT NULL, openingbalanceamount REAL NOT NULL, closingbalancedate TEXT NOT NULL, closingbalanceamount REAL NOT NULL, sequencecomplete TEXT NOT NULL, sequence TEXT NOT NULL, segment TEXT NOT NULL, statement TEXT, originalfile TEXT, FOREIGN KEY (account) REFERENCES Accounts (account), FOREIGN KEY (originalfile) REFERENCES IntegratedFiles (integratedfile));")

        elif arg2 == "INTEG": # Integrate MT940 files in database
            ### Flow description
            # validate args ?!?
            # DONE # get in file attributes
            # DONE # read file
            # DONE # split statements into list
            # DONE # save process to IntegratedFiles
            # DONE # foreach statement
            #  check account exists
            #   if not save account to Accounts
            #  check statement exists
            #   if not save statement
            #          update Accounts
            #   if yes save statementdups


            # Validate entered args

            # Read mt940 file into list of statements
            open_mt940 = psc_util.psc_read_text_file(arg4, "MT940")

            # Create IntegratedFiles record
            filedate = datetime.fromtimestamp(os.path.getmtime(arg4))
            list_values = f"('{arg4}##{filedate}', '{arg4}', '{filedate}', {len(open_mt940)}, '{datetime.now()}')"
            sqlite_connection.insert_record("IntegratedFiles", table_integrated_files, list_values)

            for i in enumerate(open_mt940):
                mt940_statement = psc_util.psc_dict_mt940(i)

                # Identify tag :25: and split statements in a list
                # If empty return error warning
                # else
                # Insert into IntegratedFiles

                # for each element in list
                # fill dictionary to prepare insert in table

                # check if statement already exists in table
                account = mt940_statement[":25:"]
                if sqlite_connection.select_record(self, "Accounts", "account", account) == None:
                    logger.debug(f"New account to create: '{account}'.")
                    list_values = f"('{account}', '{account}', '1900-01-01', 0)"
                    sqlite_connection.insert_record("Accounts", table_accounts, list_values)
                else:
                    logger.debug(f"Account already exists: '{account}'.")
                    

                # insert dicc in table
                # (first check if account exists and insert account else update account)
                # if exists insert in duplicates table

            # output all statements inserted and the duplicates
            # :25: :28C: Inserted/Duplicate

            pass

        elif arg2 == "EXTRACT": # Extract to file statements from requested account/sequence numbers
            # Read ini file with account list for account number update and other replace instructions
            pass

        elif arg2[0:3] == "LOG_": # Format LOG_#99 - list log for last n days Processes/Statements/Account
            pass

        else:
            pass

        sqlite_connection.close_conn()

