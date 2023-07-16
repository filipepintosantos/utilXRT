# psc_util.py

"""
Library for useful generic functions

@Author: Filipe Santos
"""

import psc_logging as psc_logs

def psc_read_text_file(filename, fileformat="NONE"):
    try:
        content_list = list()
        with open(filename, 'r') as file:
            if fileformat == "MT940":
                file_string = file.read()

                while file_string.find(":25:") > -1:
                    bytes_file_string = bytes(file_string, 'utf-8')
                    statement_start = bytes_file_string.find(b"{1:")
                    statement_end = bytes_file_string.find(b":25:") + bytes_file_string[bytes_file_string.find(b":25:"):].find(b"}") + 1

                    #statement = bytes.decode(bytes_file_string[statement_start:statement_end], 'utf-8')
                    statement = psc_dict_mt940(bytes_file_string[statement_start:statement_end])
                    print(statement[":25:"])
                    print(statement[":28C:"])
                    print(statement[":28C:A"])
                    print(statement[":28C:B"])
                    print(statement[":60a:"])
                    print(statement[":62a:"])
                    #print(statement[":62a:1"])
                    #print(statement[":62a:2"])
                    #print(statement[":62a:3"])
                    #print(statement[":62a:4"])

                    file_string = bytes.decode(bytes_file_string[statement_end:])
                    content_list.append(statement)
                
                if not(content_list):
                    print("No statements found in file")

            else:
                content_list = file.readlines()
                content_list = [x.strip() for x in content_list]
                if fileformat == "AFB120":
                    content_string = " ".join(line.rstrip() for line in content_list)
                    content_list = [(content_string[i:i+120]) for i in range(0, len(content_string), 120)]

        return content_list
    except FileNotFoundError as e:
        psc_logs.logger.exception(f"{e}")

def psc_dict_mt940(bytestring):
    start25 = bytestring.find(b":25:")+4
    end25 = bytestring[bytestring.find(b":25:")+4:].find(b"\n")
    start28C = bytestring.find(b":28C:")+5
    end28C = bytestring[bytestring.find(b":28C:")+5:].find(b"\n")
    if bytestring[start28C:start28C+end28C].find(b"/") > -1:
        a28C = bytestring[start28C:start28C+end28C][0:bytestring[start28C:start28C+end28C].find(b"/")]
        b28C = bytestring[start28C:start28C+end28C][bytestring[start28C:start28C+end28C].find(b"/")+1:]
    else:
        a28C = bytestring[start28C:start28C+end28C]
        b28C = b" "
    start60a = bytestring.find(b":60")+5
    end60a = bytestring[bytestring.find(b":60")+5:].find(b"\n")
    start62a = bytestring.find(b":62")+5
    end62a = bytestring[bytestring.find(b":62")+5:].find(b"\n")
    
    dict_mt940 = {
        ":25:": bytes.decode(bytestring[start25:start25+end25], 'utf-8'),
        ":28C:": bytes.decode(bytestring[start28C:start28C+end28C], 'utf-8'),
        ":28C:A": bytes.decode(a28C, 'utf-8'),
        ":28C:B": bytes.decode(b28C, 'utf-8'),
        ":60a:": bytes.decode(bytestring[start60a:start60a+end60a], 'utf-8'),
        ":60a:1": bytes.decode(bytestring[start60a:start60a+end60a][0:1], 'utf-8'),
        ":60a:2": bytes.decode(bytestring[start60a:start60a+end60a][1:7], 'utf-8'),
        ":60a:3": bytes.decode(bytestring[start60a:start60a+end60a][7:10], 'utf-8'),
        ":60a:4": bytes.decode(bytestring[start60a:start60a+end60a][10:], 'utf-8'),
        ":62a:": bytes.decode(bytestring[start62a:start62a+end62a], 'utf-8'),
        ":62a:1": bytes.decode(bytestring[start62a:start62a+end62a][0:1], 'utf-8'),
        ":62a:2": bytes.decode(bytestring[start62a:start62a+end62a][1:7], 'utf-8'),
        ":62a:3": bytes.decode(bytestring[start62a:start62a+end62a][7:10], 'utf-8'),
        ":62a:4": bytes.decode(bytestring[start62a:start62a+end62a][10:], 'utf-8'),
        "MT940": bytes.decode(bytestring, 'utf-8')
    }

    return dict_mt940


