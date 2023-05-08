# utilXRT

"""
Several validations and fixes to automate Run Procedures

@Author: Filipe Santos
"""

from array import array
from datetime import datetime
import sys
from psc_library.psc_crud_msaccess import Connect
from psc_library.psc_crud_msaccess import check_drivers
from psc_library.psc_txt_msgs import psc_msg
import psc_library.psc_logging as psc_logs
import psc_library.psc_util as psc_util

print (psc_msg("version"))
psc_logs.logger.info(psc_msg("version1"))
psc_logs.logger.info(psc_msg("version2"))

### All this should go into a module inside the library

# function convert letter to number (for last digit of AFB120 amounts)
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

# main functionality
def compare_files():
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
    psc_logs.logger.info("No Arguments assigned. Exiting")
    sys.exit()
else:
    print("List args passed. TO DO")
    pass

# begin BEFORE CATCH TEST AREA

# end BEFORE CATCH TEST AREA

try:
    # begin TEST AREA

    # end TEST AREA

    # 
    if "debug" in str(sys.argv):
        psc_logs.logger.setLevel(psc_logs.logging.getLevelName("DEBUG"))
        psc_logs.logger.info("Logging level changed to %s.", "DEBUG")

    if "license" in str(sys.argv):
        psc_logs.logger.info(f"Process argument 'license'.")
        print(psc_msg("license"))

    if "help" in str(sys.argv):
        psc_logs.logger.info(f"Process argument 'help'.")
        print(psc_msg("usage"))
        sys.exit()

    # Alternative Options - Arg 1
    if sys.argv[1] == "-c" or sys.argv[1] == "compare":
        psc_logs.logger.info(f"Process argument 'compare'.")
        compare_files()

    elif sys.argv[1] == "msaDrivers": # Check MS Access Drivers
        check_drivers()

    elif sys.argv[1] == "Rappro": # Opção Saldos Rappro
        psc_logs.logger.info(f"Process argument 'Rappro'.")
        """
        Aceder à BD Access - Check
        Aceder ao ficheiro bancário ou Excel com os extratos - Check
        Ler todas as linhas 07 - Check
        Alterar as contas identificadas na BD de saldos - Check
        """
        access_connection = Connect(sys.argv[2], "MASTER")

        print("Select before updates")
        for i, val in enumerate(access_connection.select_records("SOLDES_RIB_RAPPRO")):
            print(val)
        
        f_banque_07 = list(filter(lambda line: line[0:2] == "07", psc_util.psc_read_text_file(sys.argv[3], "BANQUE")))
        print("Lista com linhas 07 a corrigir")
        print(f_banque_07)

        list_banque = []
        for i, val in enumerate(f_banque_07):
            account_number = val[84:105]
            balance_date = datetime.strptime(val[139:147], '%Y%m%d').strftime("%d%m%y")
            balance_amount = float(val[156:173])
            print(account_number)
            psc_logs.logger.info(f"Fixing balance for Account {account_number}")
            search_account = access_connection.select_record("SOLDES_RIB_RAPPRO", 'RIB', account_number)
            if search_account == None:
                psc_logs.logger.info("Account not found in Table SOLDES_RIB_RAPPRO. Skipping.")
            else:
                print(balance_date)
                print(balance_amount)
                access_connection.update_record("SOLDES_RIB_RAPPRO", "RIB", account_number, "DATE_SOLDE", f"'{balance_date}'")
                access_connection.update_record("SOLDES_RIB_RAPPRO", "RIB", account_number, "SOLDE", balance_amount)
                access_connection.update_record("SOLDES_RIB_TRESO", "RIB", account_number, "DATE_SOLDE", f"'{balance_date}'")
                access_connection.update_record("SOLDES_RIB_TRESO", "RIB", account_number, "SOLDE", balance_amount)

        print("Select after updates")
        for i, val in enumerate(access_connection.select_records("SOLDES_RIB_RAPPRO")):
            print(val)

    elif sys.argv[1] == "RDB": # Opção Saldos RDB
        """
        Aceder à BD Access - Check
        Aceder ao ficheiro bancário ou Excel com os extratos
        Ler todas as linhas 07
        Alterar as contas identificadas na BD de saldos
        """
        #access_connection = Connect("C:\\Users\\filip\\OneDrive\\Documentos\\projects\\KProjects\\utilXRT\\external\\databases\\bd1.mdb", "MASTER")
        access_connection = Connect(sys.argv[2], "MASTER")
        print('Tabelas do banco:')
        for table in access_connection.show_tables():
            print(table.table_name)

    else:
        print(psc_msg("usage"))
        psc_logs.logger.info("No good options assigned. Exiting")
        sys.exit()

except SystemExit:
    psc_logs.logger.exception("")
except: # catch *all* exceptions
    print(psc_msg("usage"))
    psc_logs.logger.exception("")

psc_logs.logger.info("Processing finished. Exited")
sys.exit()
