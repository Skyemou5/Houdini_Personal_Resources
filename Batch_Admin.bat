if "%~1"=="" (echo *** Batch_Admin ***&echo.&echo Automatically get admin rights for another Batch. See info inside.&TIMEOUT /T 30>nul&goto:eof)

::  A D M I N I S T R A T O R   - Automatically get admin rights for script batch. Paste this on top:    net session >nul 2>nul&if errorlevel 1  Batch_Admin "%~0" %*
::                                Also keep Batch directory localisation and then set variable:   PATH_BAT
::                                if earlier variable "ShowAdminInfo" is empty (not defined) then no info, else showing info with number of seconds
::
::                                Elaboration:  Artur Zgadzaj
setlocal
setlocal DisableDelayedExpansion

SET "Localy="
if exist "%~1"      SET "Localy=YES"
if exist "%~1.BAT"  SET "Localy=YES"
if exist "%~1.CMD"  SET "Localy=YES"
if defined Localy   FOR %%I IN ("%~1") DO SET "PATH_BAT=%%~dI%%~pI"

 SET P1=%~1
 SET Parameters=%*
 SET Parameters=%Parameters:!=^^!%
setlocal EnableDelayedExpansion
 SET Parameters=!Parameters:%P1%=!
 SET Parameters=!Parameters:%%=%%%%!
setlocal DisableDelayedExpansion
 SET Parameters=%Parameters:~3%

net session >nul 2>nul&if not errorlevel 1  goto Administrator_OK

if not defined ShowAdminInfo   goto skip_message_Administrator
echo.
echo Script:  %~1
echo.
echo *****************************************************************
echo ***    R U N N I N G     A S     A D M I N I S T R A T O R    ***
echo *****************************************************************
echo.
echo Call up just as the Administrator. You can make a shortcut to the script and set:
echo.
echo          shortcut ^> Advanced ^> Running as Administrator
echo.
echo     Alternatively run once "As Administrator"
echo     or in the Schedule tasks with highest privileges
echo.
echo Cancel Ctrl-C or wait for launch  %ShowAdminInfo%  seconds ...
TIMEOUT /T %ShowAdminInfo% > nul

:skip_message_Administrator
MD %TEMP% 2> nul
SET /A $Admin$=%RANDOM% * 100 / 32768 + 1

SET "Percent="
del "%TEMP%\$Admin_%$Admin$%_Test.bat" 2>nul
echo %Parameters% > "%TEMP%\$Admin_%$Admin$%_Test.bat"
if not exist "%TEMP%\$Admin_%$Admin$%_Test.bat"  SET Percent=^"
del "%TEMP%\$Admin_%$Admin$%_Test.bat" 2>nul

echo @SET "PATH_BAT=%PATH_BAT%"               > "%TEMP%\$Admin_%$Admin$%_Batch_Start.bat"
echo @SET "BatchFullName=%BatchFullName%"    >> "%TEMP%\$Admin_%$Admin$%_Batch_Start.bat"
if defined Localy  (echo @CD /D "%PATH_BAT%" >> "%TEMP%\$Admin_%$Admin$%_Batch_Start.bat")
echo @"%~1" %Parameters% %Percent% >> "%TEMP%\$Admin_%$Admin$%_Batch_Start.bat"

echo SET UAC = CreateObject^("Shell.Application"^)                                   > "%TEMP%\$Admin_%$Admin$%_Batch_getPrivileges.vbs"
echo UAC.ShellExecute "%TEMP%\$Admin_%$Admin$%_Batch_Start.bat", "", "", "runas", 1 >> "%TEMP%\$Admin_%$Admin$%_Batch_getPrivileges.vbs"
"%TEMP%\$Admin_%$Admin$%_Batch_getPrivileges.vbs"
endlocal
exit /B

:Administrator_OK
"%~1" %Parameters%
goto:eof
REM *** A D M I N I S T R A T O R  - Automatically get admin rights  (The End)  ***
