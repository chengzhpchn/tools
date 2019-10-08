RD /S /Q build dist __pycache__
DEL Main.spec

pause

pyinstaller -F Main.py