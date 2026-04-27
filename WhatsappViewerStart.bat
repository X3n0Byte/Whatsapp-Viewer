@echo off
chcp 65001 >nul
title WhatsApp Chat Viewer

cd /d "%~dp0"

echo.
echo  +------------------------------------------+
echo  ^|       WhatsApp Chat Viewer               ^|
echo  ^|       Windows Starter                    ^|
echo  +------------------------------------------+
echo.

:: ── Python prüfen ────────────────────────────────────────────────────────────
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo  [FEHLER] Python wurde nicht gefunden!
    echo.
    echo  Bitte Python 3.9+ installieren:
    echo  https://www.python.org/downloads/
    echo.
    echo  Wichtig beim Installieren:
    echo  "Add Python to PATH" aktivieren!
    echo.
    pause
    exit /b 1
)

:: ── Python-Version prüfen (mind. 3.9) ────────────────────────────────────────
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PY_VER=%%v
for /f "tokens=1,2 delims=." %%a in ("%PY_VER%") do (
    set PY_MAJOR=%%a
    set PY_MINOR=%%b
)
if %PY_MAJOR% LSS 3 (
    echo  [FEHLER] Python 3.9 oder neuer erforderlich. Gefunden: %PY_VER%
    echo  https://www.python.org/downloads/
    pause
    exit /b 1
)
if %PY_MAJOR% EQU 3 if %PY_MINOR% LSS 9 (
    echo  [FEHLER] Python 3.9 oder neuer erforderlich. Gefunden: %PY_VER%
    echo  https://www.python.org/downloads/
    pause
    exit /b 1
)

:: ── Skript starten ───────────────────────────────────────────────────────────
python interactive.py

if %errorlevel% neq 0 (
    echo.
    echo  [FEHLER] Das Skript wurde mit einem Fehler beendet.
    echo  Bitte Screenshot machen und im GitHub-Issue melden.
    echo.
    pause
)
