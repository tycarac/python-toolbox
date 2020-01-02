@echo off
setlocal
del /s/q *.bak >nul 2>&1

set logfile=install-python-packages.log
del /q %logfile%

REM ___________________________________________________________________________
REM Create virtural environment
if not exist [.\.env] (
python -m venv ".\.env"
)
call .env\Scripts\activate

REM ___________________________________________________________________________
REM List Python packaes
set cmd=python -m pip list --no-color
echo. | tee.exe -a %logfile%
echo %cmd% | tee.exe -a %logfile%
%cmd% | tee.exe -a %logfile%

REM ___________________________________________________________________________
REM List outdated Python packaes
set cmd=python -m pip list --no-color --outdated 
echo. | tee.exe -a %logfile%
echo %cmd% | tee.exe -a %logfile%
%cmd% | tee.exe -a %logfile%

REM ___________________________________________________________________________
REM Install/update useful Python packages
REM Pip "list" output for default Python install is: "pip", "setuptools"
set cmd=python -m pip install --no-color --compile --upgrade pip setuptools
echo. | tee.exe -a %logfile%
echo %cmd% | tee.exe -a %logfile%
%cmd% | tee.exe -a %logfile%

REM ___________________________________________________________________________
REM Install/Update packeages from requirements
if not exist "requirements.txt" goto :eof

set cmd=pip.exe install --no-color --compile -U --upgrade-strategy eager -r requirements.txt
echo cmd %cmd%
echo. | tee.exe -a %logfile%
echo %cmd% | tee.exe -a %logfile%
%cmd% | tee.exe -a %logfile%
