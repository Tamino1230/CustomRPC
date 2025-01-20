@echo off

:: Variablen definieren
set "currentDir=%~dp0"
set "desktopPath=%USERPROFILE%\Desktop"
set "shortcutName=CustomRPC (ui) - @tamino1230.lnk"
set "targetFile=main_with_ui.bat"
set "iconPath=%currentDir%icon\babToma.ico"

:: Prüfen, ob die Zieldatei existiert
if not exist "%currentDir%%targetFile%" (
    echo Die Datei "%targetFile%" wurde im aktuellen Verzeichnis nicht gefunden.
    pause
    exit /b 1
)

:: Prüfen, ob das Icon existiert
if not exist "%iconPath%" (
    echo Die Datei "icon\babToma.ico" wurde im aktuellen Verzeichnis nicht gefunden.
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
echo Verknüpfung zu "%targetFile%" wurde erfolgreich auf dem Desktop erstellt.

:: Pfad der Zieldatei anzeigen
echo Zieldatei gespeichert unter: %currentDir%%targetFile%

:: Versuche, den Python-Pfad zu finden
set "pythonPath="
for /f "tokens=*" %%P in ('where python') do (
    set "pythonPath=%%P"
    goto :found
)

:notfound
echo Python wurde nicht gefunden.
pause
exit /b 1

:found
echo Der Python-Pfad ist: %pythonPath%

pip install -r requirements.txt

cd /d "%~dp0"
:: Datei mit Python öffnen
set "fileToOpen=main_with_ui.py"
if not exist "%fileToOpen%" (
    echo Die Datei "%fileToOpen%" wurde nicht gefunden.
    pause
    exit /b 1
)

echo -
echo Please wait the file is Starting..
echo Do not close the window!
echo -
"%pythonPath%" "%fileToOpen%"
pause
