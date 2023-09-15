# utilXRT

"""
Several validations and fixes to automate Run Procedures

@Author: Filipe Santos
"""

import sys
sys.path.append("psc_library")
from array import array
from datetime import datetime

import psc_library.psc_util as psc_util
from psc_library.psc_logging import logger
from psc_library.psc_txt_msgs import psc_msg

print(psc_msg("version"))
logger.info(psc_msg("version1"))
logger.info(psc_msg("version2"))

### All this should go into a module inside the library

# function convert letter to number (for last digit of AFB120 amounts) # Move this to psc_util
def psc_letter2number(letter):
    if letter in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "{"]:
        number = ord(letter)-64
        sense = "+"
    elif letter in ["J", "K", "L", "M", "N", "O", "P", "Q", "R", "}"]:
        number = ord(letter)-73
        sense = "-"
    if letter in ["{", "}"]:
        number = 0
    return number, sense

def compare_files(): # Move this to psc_util
    # call function to read file
    f_afb120_01 = list(filter(lambda line: line[0:2] == "01", psc_util.psc_read_text_file(sys.argv[2], "AFB120")))
    f_banque_01 = list(filter(lambda line: line[0:2] == "07", psc_util.psc_read_text_file(sys.argv[3], "BANQUE")))

    # build the tables
    list_afb120 = []
    list_banque = []
    for i, val in enumerate(f_afb120_01):
        number, sense = psc_letter2number(val[103:104])
        list_afb120.append(val[0:2] + ":" + val[3:7]+val[11:16]+val[21:32] + ":" + datetime.strptime(val[34:40], '%d%m%y').strftime("%Y-%m-%d") + ":" + val[16:19] + ":" + f'{float(val[90:103] + str(number))/100:.3f}' + ":" + sense)

    for i, val in enumerate(f_banque_01):
        list_banque.append(val[0:2] + ":" + val[85:105] + ":" + datetime.strptime(val[139:147], '%Y%m%d').strftime("%Y-%m-%d") + ":" + val[147:150] + ":" + f'{float(val[156:173]):.3f}' + ":" + val[173:174])

    if list_afb120 == list_banque:
        print("Validation passed - all blocks identical")
    else:
        # find difference (a - b)
        print("Differences AFB120")
        result = set(list_afb120) - set(list_banque)
        print(list(result))

        # find difference (b - a)
        print("Differences BANQUE")
        result = set(list_banque) - set(list_afb120)
        print(list(result))

# execution block
if len(sys.argv) < 1:
    logger.info("No Arguments assigned. Exiting")
    sys.exit()
else:
    logger.info("Arguments passed:")
    for i, val in enumerate(sys.argv):
        logger.info(f"Arg {i} - {sys.argv[i]}")

# main functionalities 
try:
    if "debug" in str(sys.argv):
        logger.set_level("DEBUG")

    if "license" in str(sys.argv):
        logger.info("Process argument 'license'.")
        print(psc_msg("license"))
        sys.exit()

    if "history" in str(sys.argv):
        logger.info("Process argument 'history'. Output development history.")
        print(psc_msg("history"))
        sys.exit()

    if "help" in str(sys.argv):
        logger.info("Process argument 'help' / usage.")
        print(psc_msg("usage"))

    # Alternative Options - Arg 1
    logger.info(f"Process argument '{sys.argv[1]}'.")

    if sys.argv[1] == "-c" or sys.argv[1] == "compare":
        """
        Validate if necessary arguments exist
        """
        compare_files()

    elif sys.argv[1] == "msaDrivers": # Check for installed Access Drivers
        from psc_library.psc_crud_msaccess import check_drivers
        check_drivers()

    elif sys.argv[1] == "Rappro": # Option Balances Rappro
        """
        Validate if necessary arguments exist
        Aceder à BD Access - Check
        Aceder ao ficheiro bancário ou Excel com os extratos - Check
        Ler todas as linhas 07 - Check
        Alterar as contas identificadas na BD de saldos - Check
        """
        from psc_library.psc_crud_msaccess import connectMSAccess
        access_connection = connectMSAccess(sys.argv[2], "MASTER")

        print("Select before updates")
        with open('before.txt', 'w') as f:
            for i, val in enumerate(access_connection.select_records("SOLDES_RIB_RAPPRO", 5000)):
                f.write(val)
        
        f_banque_07 = list(filter(lambda line: line[0:2] == "07", psc_util.psc_read_text_file(sys.argv[3], "BANQUE")))
        print("Lista com linhas 07 a corrigir")
        print(f_banque_07)

        for i, val in enumerate(f_banque_07):
            account_number = val[84:105]
            balance_date = datetime.strptime(val[139:147], "%Y%m%d").strftime("%Y%m%d")
            balance_amount = float(val[173:174]+val[156:173])
            print(account_number)
            print(balance_date)
            print(balance_amount)
            logger.info(f"Fixing balance for Account {account_number}")
            search_account = access_connection.select_record("SOLDES_RIB_RAPPRO", 'RIB', account_number)
            if search_account == None:
                logger.info("Account not found in Table SOLDES_RIB_RAPPRO. Skipping.")
            elif search_account[2] > balance_date:
                logger.info(f"Date in File {balance_date} < Date in Database {search_account[2]}")
                logger.info("Balance Date to update is older than Date in Database. Skipping.")
            else:
                access_connection.update_record("SOLDES_RIB_RAPPRO", "RIB", account_number, "SOLDE", balance_amount, f" and DATE_SOLDE <= '{balance_date}'")
                access_connection.update_record("SOLDES_RIB_RAPPRO", "RIB", account_number, "DATE_SOLDE", f"'{balance_date}'", f" and DATE_SOLDE <= '{balance_date}'")
                access_connection.update_record("SOLDES_RIB_TRESO", "RIB", account_number, "SOLDE", balance_amount, f" and DATE_SOLDE <= '{balance_date}'")
                access_connection.update_record("SOLDES_RIB_TRESO", "RIB", account_number, "DATE_SOLDE", f"'{balance_date}'", f" and DATE_SOLDE <= '{balance_date}'")

        print("Select after updates")
        with open('after.txt', 'w') as f:
            for i, val in enumerate(access_connection.select_records("SOLDES_RIB_RAPPRO", 5000)):
                f.write(val)

        access_connection.close_conn()

    elif sys.argv[1] == "RDB": # Option Balances RDB (REFONTE)
        """
        Validate if necessary arguments exist
        Aceder à BD Access - Check
        Aceder ao ficheiro bancário ou Excel com os extratos
        Ler todas as linhas 07
        Alterar as contas identificadas na BD de saldos
        """
        from psc_library.psc_crud_msaccess import connectMSAccess
        access_connection = connectMSAccess(sys.argv[2], "MASTER")
        table_rdb = "CONTROLE_DATE_SOLDE"

        print("Select before updates")
        with open('before.txt', 'w') as f:
            for i, val in enumerate(access_connection.select_records(table_rdb, 5000)):
                f.write(val)
        
        f_afb120_07 = list(filter(lambda line: line[0:2] == "07", psc_util.psc_read_text_file(sys.argv[3], "AFB120")))
        print("Lista com linhas 07 a corrigir")
        print(f_afb120_07)

        for i, val in enumerate(f_afb120_07):
            account_number = val[3:7]+val[11:16]+val[21:32]
            balance_date = datetime.strptime(val[34:40], "%d%m%y").strftime("%d%m%y")
            number, sense = psc_letter2number(val[103:104])
            balance_amount = float(sense + number)*100
            print(account_number)
            print(balance_date)
            print(balance_amount)
            logger.info(f"Fixing balance for Account {account_number}")
            search_account = access_connection.select_record(table_rdb, 'RIB', account_number)
            if search_account == None:
                logger.info(f"Account not found in Table {table_rdb}. Skipping.")
            elif search_account[2] > balance_date:
                logger.info(f"Date in File {balance_date} < Date in Database {search_account[2]}")
                logger.info("Balance Date to update is older than Date in Database. Skipping.")
            else:
                access_connection.update_record(table_rdb, "RIB", account_number, "SOLDE", balance_amount, f" and DATE_SOLDE <= '{balance_date}'")
                access_connection.update_record(table_rdb, "RIB", account_number, "DATE_SOLDE", f"'{balance_date}'", f" and DATE_SOLDE <= '{balance_date}'")

        print("Select after updates")
        with open('after.txt', 'w') as f:
            for i, val in enumerate(access_connection.select_records(table_rdb, 5000)):
                f.write(val)

        access_connection.close_conn()

    elif sys.argv[1] == "CtrlMT940": # Options for analysis of received MT940 statements
        from psc_library.psc_spec_ctrl_mt940 import ctrl_mt940
        ctrl_mt940(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        result = f"Process {sys.argv[1]} with option {sys.argv[2]} completed successfully."
        logger.info(result)
        print(result)
                
    elif sys.argv[1] == "CAMT054": # Options for manupulation of xml sepa files Camt054
        from psc_library.psc_xml_sepas import camt054_cacib
        camt054_cacib(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
        result = f"Process {sys.argv[1]} with option {sys.argv[2]} completed successfully."
        logger.info(result)
        print(result)

    else: # No valid options selected.
        print(psc_msg("usage"))
        logger.info("No valid options selected.")

except SystemExit as e:
    logger.exception(f"System Exit Exception: {e}")
except FileNotFoundError as e:
    logger.info("Error: File not found.")
    logger.exception(f"{e}")
except Exception as e: # catch *all* exceptions
    logger.exception(f"Unexpected Error: {e}")

logger.info("Processing finished. Exited")
sys.exit()
