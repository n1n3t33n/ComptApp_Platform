# ComptApp Platform

**Plateforme ivoirienne de comptabilité** — application web Django permettant à une petite
entreprise de gérer ses opérations financières de base : recettes, dépenses, clients et
fournisseurs, rapports comptables et sauvegarde des données.

> Projet de fin de module — Licence 2 Informatique / Gestion
> Institut Ivoirien de Technologie — Année académique 2025–2026

---

## Fonctionnalités

- **Authentification à deux facteurs (2FA)** : connexion par email + mot de passe, puis code
  de vérification à usage unique envoyé par email.
- **Rôles** : Administrateur et Agent comptable (comptes créés via l'administration Django).
- **Recettes & Dépenses** : ajout, modification, suppression, recherche multicritère.
- **Clients & Fournisseurs** : gestion unifiée des partenaires.
- **Rapports** : journal des opérations, bilan simplifié, états par catégorie, export PDF.
- **Tableau de bord** : indicateurs clés du mois et dernières opérations.
- **Sauvegarde / Restauration** : export et import des données (réservé à l'administrateur).

---

## Pile technique

| Élément | Technologie |
|---|---|
| Langage | Python 3.13 |
| Framework | Django |
| Base de données | PostgreSQL 16 |
| Front-end | HTML, CSS, JavaScript (charte BankDash) |
| Export PDF | xhtml2pdf |
| Configuration | python-dotenv (`.env`) |

---

## Installation

### 1. Prérequis

- Python 3.13+
- PostgreSQL 16 (avec pgAdmin)
- Git

### 2. Cloner le dépôt

```bash
git clone https://github.com/n1n3t33n/ComptApp_Platform.git
cd ComptApp_Platform
```

### 3. Créer et activer l'environnement virtuel

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Créer la base de données

Dans pgAdmin, créez une base nommée `comptapp_ci`.

### 6. Configurer le fichier `.env`

Créez un fichier `.env` à la racine du projet :

```env
DJANGO_SECRET_KEY=votre-cle-secrete
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=comptapp_ci
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432

OTP_VALIDITE_MINUTES=5
```

> Le fichier `.env` n'est jamais versionné (il figure dans `.gitignore`).

### 7. Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Créer un compte administrateur

```bash
python manage.py createsuperuser
```

> La connexion se fait par **email** (pas par nom d'utilisateur).

### 9. Lancer le serveur

```bash
python manage.py runserver
```

Rendez-vous sur **http://127.0.0.1:8000/**.

---

## Utilisation

1. Connectez-vous avec votre email et votre mot de passe.
2. En développement, le **code de vérification (OTP)** s'affiche dans la **console** du
   serveur (et non dans une vraie boîte email).
3. Saisissez le code pour accéder au tableau de bord.

Les comptes Administrateur et Agent se créent via l'interface d'administration :
**http://127.0.0.1:8000/admin/**

---

## Structure du projet

```
ComptApp_Platform/
├── comptapp_platform/      # Configuration du projet (settings, urls)
├── core/                   # Tableau de bord, catégories, sauvegarde
├── accounts/               # Utilisateurs, rôles, 2FA
├── partners/               # Clients & fournisseurs
├── revenues/               # Recettes
├── expenses/               # Dépenses
├── reports/                # Journal, bilan, états, export PDF
├── templates/              # Gabarits (base/ + un dossier par app)
├── static/                 # CSS, JS, images
├── requirements.txt
└── manage.py
```

Chaque application suit une convention de **packages** : les fichiers `models`, `views`,
`admin` et `forms` sont des dossiers contenant un fichier par classe/fonction.

---

## Documentation

Les documents complets du projet (au format PDF) sont fournis séparément :

- **Cahier des charges**
- **Rapport final**
- **Manuel utilisateur**

---

## Auteur

**Moussa Ben Youssouf TRAORE**
Encadrante : Mme Anna Sandrine
Institut Ivoirien de Technologie