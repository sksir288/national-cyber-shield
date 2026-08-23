@echo off
title National Cyber Shield - Master Controller
color 0A

echo ==================================================
echo   NATIONAL CYBER SHIELD - LAUNCHING SYSTEM
echo ==================================================
echo.

echo [+] Step 1: Starting Web Dashboard...
start cmd /k "python dashboard.py"

echo [+] Step 2: Launching Active Defense Engine...
start cmd /k "python packet_engine.py"

timeout /t 3 >nul

echo.
echo ==================================================
echo   SYSTEM FULLY ACTIVE AND READY FOR DEMONSTRATION
echo ==================================================
echo.
echo Press any key to run Attack Simulation Test...
pause >nul

python test_attack.py
pause