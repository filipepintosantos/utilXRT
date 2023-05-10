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
rem # use on vm - Commit if necessary then Pull
rem git commit -m "Short changes description"
rem git pull --force
rem 
