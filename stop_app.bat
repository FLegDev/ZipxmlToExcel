@echo off
echo === Arrêt du serveur Django sur le port 8000 ===

:: Récupère le PID du processus qui utilise le port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    set PID=%%a
)

:: Vérifie si un PID a été trouvé
if not defined PID (
    echo Aucun processus ne tourne sur le port 8000.
    pause
    exit /b
)

:: Tuer le processus
taskkill /f /pid %PID%

echo === Serveur arrêté (PID %PID%) ===
pause
