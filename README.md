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
- Fix negativos Rappro - OK
- Fix negativos RDB - OK
- Data no RDB é campo 4
- Mudar selects de default (10) para 5000 - OK
- Numa fase testes (ou opção debug!!) criar ficheiro com export da BD before e after - OK
- Comparar os dois e listar as diferenças
