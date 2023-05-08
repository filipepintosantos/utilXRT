call .\venv\scripts\activate
pyinstaller --onefile utilXRT.py
pyinstaller --onefile --name utilXRT(x86).exe utilXRT.py
pause

rem 
rem git commands::
rem git status
rem git add .
rem git commit -m "Short changes description"
rem git push origin master
rem 
rem git pull # use on vm
rem 
