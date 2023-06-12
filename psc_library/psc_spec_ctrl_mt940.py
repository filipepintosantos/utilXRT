# psc_spec_ctrl_mt940.py

"""
Specification Control MT940

@Author: Filipe Santos
@LastUpdate: 2023-06-09

ler extratos MT940
identificar contas, sequencias, datas, saldos e os blocos do extrato
guardar em BD SQLite (ou mySQL)
- Contas
- Sequencias / Data receção / Data Saldo / Saldos Inicial/Final?
validar se já registou o extrato (possiveis duplicados)

"""


from psc_crud_sqlite import connectSQLite
import psc_logging as psc_logs
import psc_util as psc_util

class ctrl_mt940:
    def __init__(self, arg2, arg3, arg4, arg5):
        psc_logs.logger.debug(f"Processing option: '{arg2}'.")
        psc_logs.logger.debug(f"Database: '{arg3}'.")
        psc_logs.logger.debug(f"Data in: '{arg4}'.")
        psc_logs.logger.debug(f"Data out: '{arg5}'.")
        
        sqlite_connection = connectSQLite(arg3)

        # table "Accounts" : "CREATE TABLE IF NOT EXISTS Accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, account TEXT NOT NULL, iban TEXT, laststatementdate TEXT NOT NULL, expected INT NOT NULL); CREATE UNIQUE INDEX accounts_account on accounts(account);"
        # table "IntegratedFiles" : "CREATE TABLE IF NOT EXISTS IntegratedFiles (id INTEGER PRIMARY KEY AUTOINCREMENT, integratedfile TEXT NOT NULL, filename TEXT NOT NULL, filedate TEXT NOT NULL, integrationdate TEXT NOT NULL); CREATE UNIQUE INDEX IntegratedFiles_integratedfile on IntegratedFiles(integratedfile);"
        # table "Statements" : "CREATE TABLE IF NOT EXISTS Statements (id INTEGER PRIMARY KEY AUTOINCREMENT, format TEXT NOT NULL, account TEXT NOT NULL, openingbalancedate TEXT NOT NULL, openingbalanceamount REAL NOT NULL, closingbalancedate TEXT NOT NULL, closingbalanceamount REAL NOT NULL, sequencecomplete TEXT NOT NULL, sequence TEXT NOT NULL, segment TEXT NOT NULL, statement TEXT, originalfile TEXT, FOREIGN KEY (account) REFERENCES Accounts (account), FOREIGN KEY (originalfile) REFERENCES IntegratedFiles (integratedfile));"

        if arg2 == "INTEG": # Integrate MT940 files in database
            # Read mt940 file
            open_mt940 = psc_util.psc_read_text_file(arg4, "MT940")

            # Identify tag :25: and split statements in a list
            # If empty return error warning
            # else
            # Insert into IntegratedFiles

            # for each element in list
                # fill dictionary to prepare insert in table

                # check if statement already exists in table

                # insert dicc in table
                # (first check if account exists and insert account else update account)

            # output all statements inserted and the duplicates
            # :25: :28C: Inserted/Duplicate
            pass
        elif arg3 == "LOG_L7D": # list log for last 7 days
            pass
        elif arg3 == "EXTRACT": # Extract to file statements from requested account/sequence numbers
            pass
        else:
            pass

        sqlite_connection.close_conn()
