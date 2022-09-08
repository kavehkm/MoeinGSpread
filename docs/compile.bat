pyinstaller --windowed --uac-admin --noupx --icon=resources\gsheet.ico mgs.py

xcopy  resources dist\mgs\resources /s /e /i
xcopy settings.json dist\mgs\
