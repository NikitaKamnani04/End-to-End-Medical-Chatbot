



pip check
IF %ERRORLEVEL% NEQ 0 exit /B 1
python -m conda tos --version
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
