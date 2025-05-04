# ZipxmlToExcel

ZipxmlToExcel est une application Django permettant d'importer des fichiers ZIP contenant des factures XML (SmartSign), de les parser, de visualiser les données, et de les exporter dans un fichier Excel unifié.

---

## 🔧 Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/FlegDev/ZipxmlToExcel.git
cd ZipxmlToExcel
```

### 2. Créer et activer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer les migrations Django
```bash
python manage.py migrate
```

### 5. Créer un superutilisateur (pour accéder à l'admin)
```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur de développement
```bash
python manage.py runserver
```

---

## 🚀 Utilisation

1. Connectez-vous à l’interface Django admin :  
   http://127.0.0.1:8000/admin/

2. Importer vos fichiers :
   - Accédez à la section dédiée dans l'administration Django.
   - Utilisez l'interface d'import pour charger un ou plusieurs fichiers `.zip` contenant des factures XML.
   - Les fichiers sont automatiquement extraits et analysés.

3. Export :
   - Depuis la liste des factures, utilisez l'action "Exporter en Excel".
   - Un fichier `.xlsx` est généré avec toutes les informations extraites (selon le modèle défini).

---

## 🧾 Format pris en charge

Les factures doivent être :
- au format XML SmartSign,
- regroupées dans des fichiers ZIP.

---

## 🌐 Langues

L’application adapte la langue de l’interface et des fichiers exportés (français / vietnamien) selon le profil utilisateur.

---

## 📂 Structure du projet

- `invoices/` : app principale contenant les modèles, vues, services, templates.
- `templates/` : pour les vues personnalisées (import, confirmation, etc.).
- `admin.py` : configuration de l’interface Django admin (avec actions personnalisées).
- `services.py` : logique de parsing XML et génération de fichiers Excel.

---

## ✍️ Contribuer

Les contributions sont les bienvenues ! Pour proposer une amélioration :
- Forkez le repo
- Créez une branche `feature/xxx`
- Proposez une Pull Request

---

## 📃 Licence

Ce projet est sous licence MIT.
