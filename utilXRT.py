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
#from psc_library.psc_versiondata import VersionData

print (psc_msg("version"))


# function to read txt file into list
def psc_read_txt(filename, fileformat="NONE"):
#    with open("external\\filesin\\" + filename, 'r') as file:
    with open(filename, 'r') as file:
        content_list = file.readlines()
        content_list = [x.strip() for x in content_list]
        if fileformat == "AFB120":
            content_string = " ".join(line.rstrip() for line in content_list)
            content_list = [(content_string[i:i+120]) for i in range(0, len(content_string), 120)]
        #print(content_list)

    return content_list

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
    f_afb120_01 = list(filter(lambda line: line[0:2] == "01", psc_read_txt(sys.argv[2], "AFB120")))
    f_banque_01 = list(filter(lambda line: line[0:2] == "01", psc_read_txt(sys.argv[3], "BANQUE")))

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

    elif sys.argv[1] == "-vRappro":
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
