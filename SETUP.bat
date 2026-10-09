@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
REM Setup aman: membuat environment terisolasi (.venv) di folder kerja, tanpa admin & tanpa mengubah Python milik komputer ini.
cd /d "%~dp0"
set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY (where python >nul 2>nul && set PY=python)
if not defined PY (
  echo Python tidak ditemukan. Minta panitia Python 3.9-3.12 atau Anaconda, lalu jalankan SETUP.bat lagi.
  pause
  exit /b 1
)
%PY% "%~dp0tools\setup_env.py" %*
pause
