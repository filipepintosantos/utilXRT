# utilXRT

"""
Several validations and fixes to automate Run Procedures

@Author: Filipe Santos
"""

from array import array
from datetime import datetime
#import logging
import sys
from psc_library.psc_crud_msaccess import Connect
from psc_library.psc_txt_msgs import psc_msg
from psc_library.psc_util import psc_read_text_file
#from psc_library.psc_versiondata import VersionData

print (psc_msg("version"))


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
    f_afb120_01 = list(filter(lambda line: line[0:2] == "01", psc_read_text_file(sys.argv[2], "AFB120")))
    f_banque_01 = list(filter(lambda line: line[0:2] == "07", psc_read_text_file(sys.argv[3], "BANQUE")))


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

# begin BEFORE CATCH TEST AREA

# end BEFORE CATCH TEST AREA

# execution block
try:
    # begin TEST AREA

    # end TEST AREA

    # 
    if "-license" in str(sys.argv):
        print(psc_msg("license"))

    elif "-h" in str(sys.argv):
        print(psc_msg("usage"))
        exit()
    
    elif sys.argv[1] == "-c" or sys.argv[1] == "-compare":
        compare_files()

    elif sys.argv[1] == "-vRappro": # Opção Saldos Rappro
        """
        Aceder à BD Access - Check
        Aceder ao ficheiro bancário ou Excel com os extratos - Check
        Ler todas as linhas 07 - Check
        Alterar as contas identificadas na BD de saldos
        """
        access_connection = Connect("C:\\Users\\filip\\OneDrive\\Documentos\\projects\\KProjects\\utilXRT\\external\\databases\\bd1.mdb", "MASTER")
        print('Tabelas do banco:')
        for table in access_connection.show_tables():
            print(table.table_name)
        
        f_banque_07 = list(filter(lambda line: line[0:2] == "07", psc_read_text_file("external\\filesin\\BPI.201509.txt", "BANQUE")))
        print("Lista com linhas 07 a corrigir")
        print(f_banque_07)

        list_banque = []
        for i, val in enumerate(f_banque_07):
            account_number = val[85:105]
            balance_date = datetime.strptime(val[139:147], '%Y%m%d').strftime("%Y-%m-%d")
            balance_amount = float(val[156:173])
            print(account_number)
            print(balance_date)
            print(balance_amount)

    elif sys.argv[1] == "-vRDB": # Opção Saldos RDB
        """
        Aceder à BD Access - Check
        Aceder ao ficheiro bancário ou Excel com os extratos
        Ler todas as linhas 07
        Alterar as contas identificadas na BD de saldos
        """
        access_connection = Connect("C:\\Users\\filip\\OneDrive\\Documentos\\projects\\KProjects\\utilXRT\\external\\databases\\bd1.mdb", "MASTER")
        print('Tabelas do banco:')
        for table in access_connection.show_tables():
            print(table.table_name)

    else:
        print(psc_msg("usage"))
        exit()

except SystemExit:
    pass
except: # catch *all* exceptions
    print(psc_msg("usage"))
