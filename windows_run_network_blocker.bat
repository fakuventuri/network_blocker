@echo off

set PYTHON_SCRIPT=%~dp0network_blocker.py

echo Requesting administrator privileges...
powershell -Command "Start-Process python -ArgumentList '\"%PYTHON_SCRIPT%\"' -Verb RunAs"

echo Done.