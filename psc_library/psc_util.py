# psc_util.py

"""
Library for useful generic functions

@Author: Filipe Santos
"""

def psc_read_text_file(filename, fileformat="NONE"):
    content_list = list[str]
    with open(filename, 'r') as file:
        content_list = file.readlines()
        content_list = [x.strip() for x in content_list]
        if fileformat == "AFB120":
            content_string = " ".join(line.rstrip() for line in content_list)
            content_list = [(content_string[i:i+120]) for i in range(0, len(content_string), 120)]

    return content_list
