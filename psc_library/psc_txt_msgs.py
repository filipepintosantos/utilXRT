# psc_txt_msgs.py

"""
Library for text messages

@Author: Filipe Santos
"""

from psc_library.psc_logging import logger
from psc_library.psc_versiondata import VersionData

info = VersionData()
program = info.program
version = info.version
copyright = info.copyright
copyright = ""
authors = info.authors
last_update = info.last_update

def psc_msg(msg_code):
    log_msg = "psc_txt_msgs.py called with msg_code = "+msg_code

    # standard version message
    if msg_code == "version":
        message  = program+" - "+version+" - "+copyright+"\n"+authors+" - "+last_update[0:7]+"\n"

    elif msg_code == "version1":
        message  = program+" - "+version +" - "+copyright
    elif msg_code == "version2":
        message  = authors+" - "+last_update[0:7]

    # standard history message
    elif msg_code == "history":
        # read&print version_history
        pass

    # standard license message
    elif msg_code == "license":
        message  = "\nMIT License\n\n" + copyright + " [" + program + " - " + authors + "]"
        message += "\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of \nthis software and associated documentation files (the ""Software""), to deal in the \nSoftware without restriction, including without limitation the rights to use, \ncopy, modify, merge, publish, distribute, sublicense, and/or sell copies of the \nSoftware, and to permit persons to whom the Software is furnished to do so, \nsubject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all \ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, \nINCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A \nPARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT \nHOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION \nOF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE \nSOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n"

    # standard usage message - change message according to arg2
    elif msg_code == "usage":
        message  = "\nUsage: utilXRT main_option [option_args]\nType utilXRT help for help (this message)\nType utilXRT license for full MIT License\n\nOptions:\n\n"
        message += "utilXRT CAMT054 CACIB sqlite_database file_in file_out (validate XSD Y/N) (XSD used in validation) (debug)"

    else:
        logger.debug("Message called with invalid argument.")

    return message
