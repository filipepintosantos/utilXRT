call .\venv\scripts\activate
pyinstaller --onefile utilXRT.py
pyinstaller --onefile --name utilXRT32.exe utilXRT.py
pause

rem 
rem git commands::
rem git status
rem git add .
rem git commit -m "Short changes description"
rem git push origin master
rem 
rem rem # use on vm (32bit) - Commit if necessary then Pull
rem git commit -m "Short changes description"
rem git pull --force
rem 

rem ### CREATE VIRTUAL ENVIRONMENT - Done only once on project creation
rem # pip install virtualenv
rem # cd KProjects\utilXRT
rem # virtualenv venv

rem ### ACTIVATE VIRTUAL ENVIRONMENT - Done everytime VSC is started
rem # cd KProjects\utilXRT
rem # .\venv\scripts\activate

rem ### UPDATE requirements.txt
rem # pip freeze > requirements.txt

rem ### INSTALL FROM requirements.txt
rem # pip install -r requirements.txt

rem ### INSTALL NEEDED LIBRARIES
rem # pip install PyInstaller
rem # pip install ...

rem ### CREATE .EXE
rem # call .\venv\scripts\activate
rem # pyinstaller utilXRT.py
rem # OR
rem # pyinstaller --onefile utilXRT.py

rem ### RUN PROGRAM SCRIPT ### RUN PROGRAM SCRIPT ### RUN PROGRAM SCRIPT ###
rem # python utilXRT.py -c external\filesin\BPI.a0 external\filesin\BPI.201509.txt
rem # python utilXRT.py Rappro external\databases\bd1.mdb external\filesin\BPI.201509.txt debug

rem ### Options for MT940
rem # INIT_DB
rem # python utilXRT.py CtrlMT940 INIT_DB external\databases\mt940demo.db filler filler debug
rem # INTEG
rem # python utilXRT.py CtrlMT940 INTEG external\databases\mt940demo.db external\filesin\MT940\Mzn_A12.MT940 filler debug
rem # EXTRACT
rem # CLEAR_DUPS
rem # LOG_L7D
rem # python utilXRT.py CtrlMT940 INTEG external\databases\mt940.db external\filesin\MT940\Mzn_A12.MT940 external\filesout\test.txt debug

rem ### Options for CAMT054
rem # CACIB
rem # python utilXRT.py CAMT054 CACIB external\databases\camt54demo.db external\filesin\XML\CAMT054\camt054_demo.xml external\filesout\XML\CAMT054\camt054_demo_out.xml N external\filesin\XML\XSD\camt.054.001.02.xsd debug

rem ### TESTS TESTS TESTS TESTS TESTS TESTS TESTS TESTS TESTS TESTS TESTS ###
rem # cd tests
rem # pytest
rem # pytest --cov=utilXRT
rem # cd ..

