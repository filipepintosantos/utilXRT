# psc_util.py

"""
Library for useful generic functions

@Author: Filipe Santos
"""

import psc_logging as psc_logs

def psc_read_text_file(filename, fileformat="NONE"):
    try:
        content_list = list[str]
        with open(filename, 'r') as file:
            if fileformat == "MT940":
                file_string = file.read()
                print("######")
                print(file_string)
                print("######")
                print("Read the MT940 - about to start spliting block in the list")

                account = file_string.find(":25:")
                print(account)

            else:
                content_list = file.readlines()
                content_list = [x.strip() for x in content_list]
                if fileformat == "AFB120":
                    content_string = " ".join(line.rstrip() for line in content_list)
                    content_list = [(content_string[i:i+120]) for i in range(0, len(content_string), 120)]

        return content_list
    except FileNotFoundError as e:
        psc_logs.logger.exception(f"{e}")

def psc_dict_mt940(string):
    dict_mt940 = {
        ":25:": "",
        ":28C:": "",
        ":28C:A": "",
        ":28C:B": "",
        ":60a:": "",
        ":60a:1": "",
        ":60a:2": "",
        ":60a:3": "",
        ":60a:4": "",
        ":62a:": "",
        ":62a:1": "",
        ":62a:2": "",
        ":62a:3": "",
        ":62a:4": "",
        "MT940": string
    }

    return dict_mt940