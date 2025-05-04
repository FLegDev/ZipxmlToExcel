@echo off
echo === Démarrage de l'application ===
call .venv\Scripts\activate.bat
start http://127.0.0.1:8000/admin

:: Démarrage du serveur en arrière-plan et enregistrement du PID
start "DjangoServer" /min cmd /c "python manage.py runserver" 
:: Petite pause pour laisser le temps au processus de démarrer
timeout /t 2 >nul

:: Récupérer le PID du processus python lancé par runserver
for /f "tokens=2 delims=," %%a in ('tasklist /fi "imagename eq python.exe" /fo csv /nh') do (
    echo %%a > server.pid
    goto done
)
:done

pause
