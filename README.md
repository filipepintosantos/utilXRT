### utilXRT
Pinto Santos - utilXRT

Several validations and fixes to automate Run Procedures



### Development plan
- CAMT054 fixer - create Ntry's for each TxDtls

- Everything below this line is for second plan
-
- MT940 Manager
- read MT940 from file
- write MT940 to file - with criteria Account / Sequence / Date - options recode account
- save MT940 to database - no duplicates - key Account + Statement Sequence
- list from database by account / statement sequence - with criteria Account / Sequence / Date
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
- Fix negativos Rappro - OK
- Fix negativos RDB - OK
- Data no RDB é campo 4
- Mudar selects de default (10) para 5000 - OK
- Numa fase testes (ou opção debug!!) criar ficheiro com export da BD before e after - OK
- Comparar os dois e listar as diferenças
