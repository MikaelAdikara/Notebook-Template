@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
REM Buka Jupyter memakai environment terisolasi (.venv) yang dibuat SETUP.bat. Folder awal = folder kerja.
cd /d "%~dp0.."
if not exist ".venv\Scripts\python.exe" (
  echo Environment belum ada. Jalankan SETUP.bat dulu.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m jupyter notebook
pause
