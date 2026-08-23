@echo off
title National Cyber Shield - Production Defense System
color 0A

echo =========================================================
echo  NATIONAL CYBER SHIELD - PRODUCTION ACTIVE DEFENSE ENGINE
echo =========================================================
echo.

echo [+] Step 1: Starting Web Monitoring Dashboard...
start "Cyber Shield Web Dashboard" cmd /k "python -m http.server 8080"

echo [+] Step 2: Launching Kernel AI Defense Engine...
start "Cyber Shield Defense Core" cmd /k "python packet_engine.py"

echo.
echo =========================================================
echo  SYSTEM FULLY ACTIVE AND PROTECTING NETWORK INFRASTRUCTURE
echo =========================================================
echo.
echo [!] Monitoring active traffic on Port 9999.
echo [!] Access visual dashboard at http://localhost:8080