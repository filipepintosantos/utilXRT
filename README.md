### utilXRT
Pinto Santos Consultores - utilXRT

Several validations and fixes to automate Run Procedures

1 compare AFB120 with XRT banque format (after manual conversion)

2 Validate (and fix) RDB balances
3 Validate (and fix) Rappro balances

4 Find (and extract) account in file (AFB120 / banque / MT940)
5 Find (and extract) bad blocks in file (AFB120 / banque)

6 Validate SCT SDD ?


### Development plan
- use pytest !!!
- use docstrings !!!
- use autosemver ???
- improve project structure
- #done# read AFB120 (arg 0)
- #done# break AFB120 file into lines of 120 char
- #done# read banque (arg 1)
- #done# compare all instances of line 01 (account, date, balance)
- setup command line activation
-   #done# deal with arguments
-   #done# argument -h for instructions
- #done# identify amount signal in AFB120
- logging to everything
- save files to database?
- save output to file or database?
- review arguments - first arg is for identifying the process to run
- automate versioning #.#.# ?
- review arguments definition - update help info
- version 2 - validate AFB120 blocks
- options: find account - extract account>; validate blocks; extract bad blocks
- version 3 - check MT940 with banque
-   #done# connect to MS Access
- 

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

### RUN PROGRAM SCRIPT
# python utilXRT.py -c external\filesin\BPI.a0 external\filesin\BPI.201509.txt
# python utilXRT.py -vRappro
