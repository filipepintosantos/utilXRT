# psc_crud_msaccess.py

"""
CRUD to manipulate MS Access database

@Author: Filipe Santos

Thanks to Renato Cruz (https://gist.github.com/natorsc/0e1d637a3dc9f2a6b2488794fffe338a)

MS Access Drivers (2023/03):
Driver Access 2010 <https://www.microsoft.com/en-US/download/details.aspx?id=13255>
Driver Access 2016 <https://www.microsoft.com/en-us/download/details.aspx?id=54920>
"""

import psutil
import pyodbc
import os
import psc_library.psc_logging as psc_logs

def check_drivers():
    #print([x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')])
    print([x for x in pyodbc.drivers()])
    psc_logs.logger.debug([x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')])

class Connect:
    def __init__(self, database, password):
        psc_logs.logger.debug("Connecting to MS Access database file:")
        if database.find(':') < 0:
            self.db = os.getcwd() + "\\" + database
        else:
            self.db = database

        self.pw = password
        self.driver = "{Microsoft Access Driver (*.mdb, *.accdb)}"
        ###
        ### get full path to database if database doesn't have a ':'
        ### put this inside a try catch for possible errors
        ###           file not found
        ###           driver not present
        ###

        psc_logs.logger.debug(rf"DRIVER={self.driver}; " rf"DBQ={self.db}; " rf"PWD={self.pw};")
        self.conn = pyodbc.connect(rf"DRIVER={self.driver}; " rf"DBQ={self.db}; " rf"PWD={self.pw};")
        #self.conn = pyodbc.connect("DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ="+database+"; PWD="+password+";")

        # ODBC User DSN
        #self.conn = pyodbc.connect(f"DSN={database}")

        self.cur = self.conn.cursor()
        psc_logs.logger.info("Connected to MS Access database file:") # Change this if it works
        psc_logs.logger.info(self.db)
        
    def show_tables(self):
        return self.cur.tables(tableType='TABLE')

    def show_attributes(self, table):
        return self.cur.columns(table)

    def close_conn(self):
        return self.conn.close()

    #CRUD - CREATE - READ - UPDATE - DELETE
    #Create
    def insert(self, table, attributes, values):
        try:
            psc_logs.logger.debug("Processing insert")
            psc_logs.logger.debug(f"INSERT INTO {table} {attributes} VALUES {values}")
            self.cur.execute(f"INSERT INTO {table} {attributes} VALUES {values}")
        except Exception as e:
            psc_logs.logger.debug(f"Error inserting record: {e}")
            self.conn.rollback()
            psc_logs.logger.debug("Operation Reversed (rollback)")
        else:
            self.conn.commit()
            psc_logs.logger.debug("Record inserted successfully!")

    def insert_multiple(self, data):
        """ Adiciona varias linhas na tabela.
        Desta forma não se faz necessário um laço de repetição com vários ``inserts``.
        :param dados: (list) lista contendo tuplas (tuple) com os dados que serão inseridos.
        """
        try:
            psc_logs.logger.debug("Processing insert multiple")
            psc_logs.logger.debug(f"Data supplied {data}")
            self.cur.executemany('''INSERT INTO NomeDaTabela (nome, idade, sexo) VALUES (?, ?, ?)''', data)
        except Exception as e:
            print('\n[x] Error inserting record [x]\n')
            print(f'[x] Reverting operation (rollback) [x]: {e}\n')
            self.conn.rollback()
        else:
            self.conn.commit()
            print('\n[!] Record inserted successfully [!]\n')

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
    def update_record(self, table, key_attribute, key_value, attribute, value):
        try:
            psc_logs.logger.debug("Processing update")
            psc_logs.logger.debug(f"UPDATE {table} SET {attribute} = {value} WHERE {key_attribute} = '{key_value}'")
            self.cur.execute(f"UPDATE {table} SET {attribute} = {value} WHERE {key_attribute} = '{key_value}'")
        except Exception as e:
            psc_logs.logger.debug(f"Error updating record: {e}")
            self.conn.rollback()
            psc_logs.logger.debug("Operation Reversed (rollback)")
        else:
            self.conn.commit()
            psc_logs.logger.debug("Record updated successfully!")

    #Delete
    def delete_record(self, table, attribute, value):
        try:
            psc_logs.logger.debug("Processing delete")
            psc_logs.logger.debug(f"DELETE FROM {table} WHERE {attribute}='{value}'")
            self.cur.execute(f"DELETE FROM {table} WHERE {attribute}='{value}'")
        except Exception as e:
            psc_logs.logger.debug(f"Error deleting record: {e}")
            self.conn.rollback()
            psc_logs.logger.debug("Operation Reversed (rollback)")
        else:
            self.conn.commit()
            psc_logs.logger.debug("Record deleted successfully!")

if __name__ == '__main__':
    # Verificar se o driver está instalado.
    # Se for retornada uma lista vazia o driver precisa ser instalado.
    print([x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')])

    # Criando a conexão com o banco.
    dbaccess = Connect("C:\\Users\\filip\\OneDrive\\Documentos\\projects\\KProjects\\external\\utilXRT\\external\\databases\\bd1.mdb", "MASTER")

###TESTS >>> MOVE INTO TESTS AREA <<<

    ### Exibindo as tabelas que estão no banco.
    print('Tabelas do banco:')
    for table in dbaccess.show_tables():
        print(table.table_name)
        
    ### Exibindo as colunas de uma tabela;
    #print('\nColunas da tabela CONTROLE_DATE_SOLDE:')
    #for coluna in dbaccess.show_attributes(table="CONTROLE_DATE_SOLDE"):
    #    print(coluna.column_name)

    #print('\nColunas da tabela SOLDES_RIB_RAPPRO:')
    #for coluna in dbaccess.show_attributes(table="SOLDES_RIB_RAPPRO"):
    #    print(coluna.column_name)

    #print('\nColunas da tabela SOLDES_RIB_TRESO:')
    #for coluna in dbaccess.show_attributes(table="SOLDES_RIB_TRESO"):
    #    print(coluna.column_name)

    ### Dados
    #data = "('018200000014128864123', 'EUR', '300323', 0)"
    #multidata = ["('018200000014213459778', 'EUR', '300323', 1000)", "('018200000014123456789', 'EUR', '300323', 65481.21)"]

    ### Inserindo um registro tabela.
    #dbaccess.insert("SOLDES_RIB_TRESO", "(RIB, DEVISE, DATE_SOLDE, SOLDE)", data)

    ### Inserindo vários registros na tabela.
    #banco.inserir_varios_registros(dados=usuarios)

    ### Consultando com filtro.
    #print(dbaccess.select_record("SOLDES_RIB_TRESO", 'RIB', '000120000008026488821'))

    ### Consultando todos (limit=10).
    #print(dbaccess.select_records("SOLDES_RIB_RAPPRO"))

    ### Alterando registro da tabela.
    ### Antes da alteração.
    #print(dbaccess.select_record("SOLDES_RIB_TRESO", 'RIB', '000120000008026488821'))
    ### Realizando a alteração.
    #dbaccess.update_record('SOLDES_RIB_TRESO', 'RIB', '000120000008026488821', 'DATE_SOLDE', '300323')
    #dbaccess.update_record('SOLDES_RIB_TRESO', 'RIB', '000120000008026488821', 'SOLDE', 90456.4)
    ### Depois da alteração.
    #print(dbaccess.select_record("SOLDES_RIB_TRESO", 'RIB', '000120000008026488821'))

    ### Removendo registro da tabela.
    ### Antes da remoção.
    #print(dbaccess.select_records("SOLDES_RIB_TRESO"))
    ### Realizando a remoção.
    #dbaccess.delete_record("SOLDES_RIB_TRESO", 'RIB', '018200000014128864123')
    ### Depois da remoção.
    #print(dbaccess.select_records("SOLDES_RIB_TRESO"))

    #print(dbaccess.close_conn())

    #for proc in psutil.process_iter():
    #    print(proc.open_files())
