# psc_xml_sepas.py

"""
Manipulation of SEPA XML files

@Author: Filipe Santos
@LastUpdate: 2023-09-09

project 1 - CAMT054 from CACIB:
we need to change the sructure of the xml to add Ntry tags for each Txdtls tag

read file to bytestring
break to save to database as lines header / transactions / footer
update lines transactions
save to file

"""

import os
from datetime import datetime
import psc_util as psc_util
from psc_crud_sqlite import connectSQLite
from psc_crud_sqlite import check_database
from psc_logging import logger

class camt054_cacib:
    def __init__(self, arg2, arg3, arg4, arg5, arg6="N", arg7=None):
        logger.info(f"Processing option: '{arg2}'.")
        logger.info(f"Database: '{arg3}'.")
        logger.info(f"XML in: '{arg4}'.")
        logger.info(f"XML out: '{arg5}'.")
        logger.info(f"Validate XML (Y/N): '{arg6}'.")
        logger.info(f"XSD: '{arg7}'.")
        
        sqlite_connection = connectSQLite(arg3)

        # table "camt054" : "CREATE TABLE IF NOT EXISTS Camt054 (id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT NOT NULL, file_date TEXT NOT NULL, document_number INT NOT NULL, line_number INT NOT NULL, line_type TEXT NOT NULL, value_original TEXT NOT NULL, value_final TEXT NOT NULL)"
        # table "camt054_archive" : "CREATE TABLE IF NOT EXISTS Camt054_archive (id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT NOT NULL, file_date TEXT NOT NULL, document_number INT NOT NULL, line_number INT NOT NULL, line_type TEXT NOT NULL, value_original TEXT NOT NULL, value_final TEXT NOT NULL)"
        # id INTEGER PRIMARY KEY AUTOINCREMENT, 
        # 
        table_camt054 = ("file_name", "file_date", "document_number", "line_number", "line_type", "value_original", "value_final")
        #table_camt054_archive = ("file_name", "file_date", "document_number", "line_number", "line_type", "value_original", "value_final")

        sqlite_connection.drop_table("camt054")
        sqlite_connection.create_table("camt054", "CREATE TABLE IF NOT EXISTS Camt054 (id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT NOT NULL, file_date TEXT NOT NULL, document_number INT NOT NULL, line_number INT NOT NULL, line_type TEXT NOT NULL, value_original TEXT NOT NULL, value_final TEXT NOT NULL)")
        sqlite_connection.create_table("camt054_archive", "CREATE TABLE IF NOT EXISTS Camt054_archive (id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT NOT NULL, file_date TEXT NOT NULL, document_number INT NOT NULL, line_number INT NOT NULL, line_type TEXT NOT NULL, value_original TEXT NOT NULL, value_final TEXT NOT NULL)")

        #Read xml file into list
        document_number = 0
        xml_camt54_in = psc_util.psc_read_text_file(arg4, "XML")
        file_name = os.path.basename(arg4).split('/')[-1]
        print(f"File name: {file_name}")
        file_date = datetime.fromtimestamp(os.path.getmtime(arg4)).strftime("%Y/%m/%d")
        print(f"File system date: {file_date}")
        for camt54 in xml_camt54_in:
            camt54 = camt54
            document_number += 1
            line_number = 0
            line_type = "H"
            count_ntry = camt54.count("<Ntry>")
            count_txdtls = camt54.count("<TxDtls>")
            logger.debug(f"Ntry: {count_ntry}, TxDtls: {count_txdtls}")

            #Check if camt54 has transactions Ntry/TxDtls
            if camt54.find("<TxDtls>") < 0 or camt54.count("<Ntry>") == camt54.count("<TxDtls>"):
                logger.debug("camt54 has no transactions to process - direct save")
                list_values = f"('{file_name}', '{file_date}', '{document_number}', '{line_number}', '{line_type}', '{camt54}', '{camt54}')"
                sqlite_connection.insert_record("camt054", table_camt054, list_values)
            else:
                logger.debug("Need to process transactions")

                # get header and insert to table
                camt54_header = camt54[0:camt54.find("<Ntry>")]
                camt54_remain = camt54[camt54.find("<Ntry>"):]

                # fix header Ntry count => TxDtls count
                camt54_header_fixed = camt54_header.replace(f"<NbOfNtries>{count_ntry}</NbOfNtries>", f"<NbOfNtries>{count_txdtls}</NbOfNtries>")

                list_values = f"('{file_name}', '{file_date}', '{document_number}', '{line_number}', '{line_type}', '{camt54_header}', '{camt54_header_fixed}')"
                sqlite_connection.insert_record("camt054", table_camt054, list_values)

                # break file by Ntry's
                line_type = "B"
                while camt54_remain.find("<Ntry>") > -1:
                    camt54_ntry = camt54_remain[0:camt54_remain.find("</Ntry>") + 7]
                    camt54_remain = camt54_remain[camt54_remain.find("</Ntry>") + 7:]

                    # get Ntry's info
                    count_ntry_txdtls = camt54_ntry.count("<TxDtls>")
                    camt54_ntry_head = camt54_ntry[0:camt54_ntry.find("<TxDtls>")]
                    camt54_ntry = camt54_ntry[camt54_ntry.find("<TxDtls>"):]

                    # get TxDtls's info
                    while camt54_ntry.find("<TxDtls>") > -1:
                        line_number += 1
                        camt54_txdtls = camt54_ntry[0:camt54_ntry.find("</TxDtls>") + 9]
                        camt54_ntry = camt54_ntry[camt54_ntry.find("</TxDtls>") + 9:]
                        
                        # fix TxDtls count in Ntry => 1 and amount = TxDtls amount
                        amount_locator = camt54_ntry_head[camt54_ntry_head.find("</NtryRef><Amt")+10:]
                        ntry_amount = amount_locator[amount_locator.find(">")+1:amount_locator.find("</Amt")]
                        amount_locator = camt54_txdtls[camt54_txdtls.find("<InstdAmt><Amt")+10:]
                        txdtls_amount = amount_locator[amount_locator.find(">")+1:amount_locator.find("</Amt")]

                        camt54_ntry_txdtls = camt54_ntry_head + camt54_txdtls + "</NtryDtls>"
                        camt54_txdtls_fixed  = camt54_ntry_head.replace(f"<NbOfTxs>{count_ntry_txdtls}</NbOfTxs>", f"<NbOfTxs>1</NbOfTxs>")
                        camt54_txdtls_fixed  = camt54_txdtls_fixed.replace(ntry_amount, txdtls_amount)
                        camt54_txdtls_fixed += camt54_txdtls + "</NtryDtls>"
                    
                        list_values = f"('{file_name}', '{file_date}', '{document_number}', '{line_number}', '{line_type}', '{camt54_ntry_txdtls}', '{camt54_txdtls_fixed}')"
                        sqlite_connection.insert_record("camt054", table_camt054, list_values)

                # get footer and insert to table
                line_type = "F"
                line_number = line_number + 1
                list_values = f"('{file_name}', '{file_date}', '{document_number}', '{line_number}', '{line_type}', '{camt54_remain}', '{camt54_remain}')"
                sqlite_connection.insert_record("camt054", table_camt054, list_values)

            #Validate xml
            if arg7 == "Yes":
                from xsd_validator import XsdValidator
                #from lxml import etree
                validator = XsdValidator(arg6)
                print(validator.assert_valid(camt54))
                print("")
                #print("XML Errors list")
                #for err in validator(camt54):
                #    logger.info(f"Error: '{err}'.")

        #Extract records from table and save xml to file
        table_lines = sqlite_connection.select_records("camt054", "value_final", "document_number, line_number, id", None)
        lines = [item[0].replace("''", "'")+"\n" for item in table_lines]
        #print(lines)
        xml_camt54_out = open(arg5, 'w')
        xml_camt54_out.writelines(lines)
        xml_camt54_out.close()

        sqlite_connection.free_query("INSERT INTO camt054_archive (file_name, file_date, document_number, line_number, line_type, value_original, value_final) SELECT file_name, file_date, document_number, line_number, line_type, value_original, value_final FROM camt054")
        sqlite_connection.close_conn()
