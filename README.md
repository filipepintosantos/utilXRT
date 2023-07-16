### utilXRT
Pinto Santos Consultores - utilXRT

Several validations and fixes to automate Run Procedures

1 compare AFB120 with XRT banque format (after manual conversion)

2 Validate (and fix) Rappro balances
3 Validate (and fix) RDB balances

4 Find (and extract) account in file (AFB120 / banque / MT940)
5 Find (and extract) bad blocks in file (AFB120 / banque)

6 Validate SCT SDD ?


### Development plan
- MT940 Manager
- read MT940 from file
- write MT940 to file - with criteria Account / Sequence / Date - options recode account
- save MT940 to database - no duplicates - key Account + Statement Sequence
- list from database by account / statement sequence - with criteria Account / Sequence / Date
- 
- Everything below this line is for second plan
- 
- improve project structure
- use pytest !!!
- use docstrings !!!
- use autosemver ???
- - automate versioning #.#.# ?
- use logging !!!
- use psutil - in logging to add info about system usage
- 
- get full path for msaccess database ##DONE##
- Convert help message into read from text file
- Pass crud_msaccess tests to Test Area
- 
- save files to database?
- save output to file or database?
- review arguments definition - update help info
- version 2 - validate AFB120 blocks
- options: find account - extract account>; validate blocks; extract bad blocks
- version 3 - check MT940 with banque
- 
- URGENT DEVELOPMENT for version 1.4.0
- Fix negativos Rappro - OK
- Fix negativos RDB - OK
- Data no RDB é campo 4
- Mudar selects de default (10) para 5000 - OK
- Numa fase testes (ou opção debug!!) criar ficheiro com export da BD before e after - OK
- Comparar os dois e listar as diferenças

### CREATE VIRTUAL ENVIRONMENT
# pip install virtualenv
# cd KProjects\utilXRT
# virtualenv venv

### ACTIVATE VIRTUAL ENVIRONMENT
# cd KProjects\utilXRT
# .\venv\scripts\activate

### UPDATE requirements.txt
# pip freeze > requirements.txt

### INSTALL FROM requirements.txt
# pip install -r requirements.txt

### INSTALL NEEDED LIBRARIES
# pip install PyInstaller
# pip install ...

### CREATE .EXE
# call .\venv\scripts\activate
# pyinstaller utilXRT.py
# OR
# pyinstaller --onefile utilXRT.py

### RUN PROGRAM SCRIPT ### RUN PROGRAM SCRIPT ### RUN PROGRAM SCRIPT ###
# python utilXRT.py -c external\filesin\BPI.a0 external\filesin\BPI.201509.txt
# python utilXRT.py Rappro external\databases\bd1.mdb external\filesin\BPI.201509.txt debug

### Options for MT940
# INIT_DB
# python utilXRT.py CtrlMT940 INIT_DB external\databases\mt940test.db filler filler debug
# INTEG
# python utilXRT.py CtrlMT940 INTEG external\databases\mt940.db external\filesin\MT940\Mzn_A12.MT940 external\filesout\test.txt debug
# EXTRACT
# CLEAR_DUPS
# LOG_L7D
# python utilXRT.py CtrlMT940 INTEG external\databases\mt940.db external\filesin\MT940\Mzn_A12.MT940 external\filesout\test.txt debug

### TESTS TESTS TESTS TESTS TESTS TESTS TESTS TESTS TESTS TESTS TESTS ###
# cd tests
# pytest
# pytest --cov=utilXRT
# cd ..
