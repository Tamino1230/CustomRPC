@echo off

:: Variablen definieren
set "currentDir=%~dp0"
set "desktopPath=%USERPROFILE%\Desktop"
set "shortcutName=CustomRPC(cmd) - @tamino1230.lnk"
set "targetFile=main.bat"
set "iconPath=%currentDir%icon\babToma.ico"

:: Prüfen, ob die Zieldatei existiert
if not exist "%currentDir%%targetFile%" (
    echo The File "%targetFile%" was not found.
    pause
    exit /b 1
)

:: Prüfen, ob das Icon existiert
if not exist "%iconPath%" (
    echo The file "icon\babToma.ico" was not found.
    pause
    exit /b 1
)

:: Eine Verknüpfung auf dem Desktop erstellen (mit VB Script)
set "folderpath=%~dp0"
set "desktop=%USERPROFILE%\Desktop"
set "shortcut=%desktop%\%shortcutName%"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\CreateShortcut.vbs"
echo sLinkFile = "%shortcut%" >> "%temp%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\CreateShortcut.vbs"
echo oLink.TargetPath = "%folderpath%%targetFile%" >> "%temp%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%folderpath%" >> "%temp%\CreateShortcut.vbs"
echo oLink.IconLocation = "%iconPath%" >> "%temp%\CreateShortcut.vbs"
echo oLink.Save >> "%temp%\CreateShortcut.vbs"

cscript //nologo "%temp%\CreateShortcut.vbs"
del "%temp%\CreateShortcut.vbs"

:: Erfolgsnachricht
echo "%targetFile%" created/updated.

:: Pfad der Zieldatei anzeigen
echo saved under: %currentDir%%targetFile%

:: Versuche, den Python-Pfad zu finden
set "pythonPath="
for /f "tokens=*" %%P in ('where python') do (
    set "pythonPath=%%P"
    goto :found
)

:notfound
echo Python was not Found! You can download it on the Microsoft Store (python 3.12.6)
pause
exit /b 1

:found
echo The Python Path is: %pythonPath%

pip install -r requirements.txt

cd /d "%~dp0"
:: Datei mit Python öffnen
set "fileToOpen=main.py"
if not exist "%fileToOpen%" (
    echo The file "%fileToOpen%" was not found.
    pause
    exit /b 1
)

echo -
echo Please wait the file is Starting..
echo Do not close the window!
echo -
"%pythonPath%" "%fileToOpen%"
pause
