@echo off
echo === Création de l'environnement virtuel ===
python -m venv .venv

echo === Activation de l'environnement virtuel ===
call .venv\Scripts\activate.bat

echo === Installation des dépendances ===
pip install -r requirements.txt

echo === Application des migrations ===
python manage.py migrate

echo === Lancement du serveur Django ===
start http://127.0.0.1:8000/admin
python manage.py runserver

pause
