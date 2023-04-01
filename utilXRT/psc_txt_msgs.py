# psc_txt_msgs.py

"""
Library for text messages

@Author: Filipe Santos
"""

from utilXRT.psc_versiondata import VersionData

info = VersionData()
program = info.program
version = info.version
copyright = info.copyright
authors = info.authors

def psc_msg(msg_code):
    # standard usage message
    if msg_code == "usage":
        message = program + " :: " + version + "\n" + copyright + "\n"
        message += "Usage: utilXRT -option file.one file.two\nType utilXRT -help for help\nType utilXRT -license for full MIT License\n\nOptions:\n   -c or -compare - compare accounts and final balances between file AFB120 and Banque.\n"


    # standard license message
    if msg_code == "license":
        message  = "\nMIT License\n\n" + copyright + " [" + program + " - " + authors + "]"
        + "\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of \nthis software and associated documentation files (the ""Software""), to deal in the \nSoftware without restriction, including without limitation the rights to use, \ncopy, modify, merge, publish, distribute, sublicense, and/or sell copies of the \nSoftware, and to permit persons to whom the Software is furnished to do so, \nsubject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all \ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, \nINCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A \nPARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT \nHOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION \nOF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE \nSOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n"

    return message
