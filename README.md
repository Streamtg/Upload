# Upload Metadata Change Bot 🤖

Bot Python pour automatiser le téléchargement, la modification de métadonnées et l’upload de fichiers.

## Fonctionnalités

- Téléchargement de fichiers avec gestion avancée
- Modification et upload de fichiers (support ffmpeg)
- Gestion des métadonnées et des messages
- Petite base de données Firebase Realtime
- Architecture modulaire

## ⚙️ Installation
<details>
<summary><h3>
- <b> ᴍᴇᴛʜᴏᴅᴇꜱ ᴅᴇ ᴅᴇᴘʟᴏʏᴇᴍᴇɴᴛ 👨🏾‍💻 </b>
</h3>
</summary>
<h3 align="center">
    ─「 ᴅᴇᴘʟᴏʏᴇʀ ꜱᴜʀ ʜᴇʀᴏᴋᴜ 」─
</h3>

<p align="center"><a href="https://heroku.com/deploy">
  <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy On Heroku"></a>
</p>
<h3 align="center">
    ─「 ᴅᴇᴘʟᴏʏᴇʀ ꜱᴜʀ ʜᴇʀᴏᴋᴜ 」─
</h3>
<p align="center"><a href="https://app.koyeb.com/deploy">
  <img src="https://www.koyeb.com/static/images/deploy/button.svg" alt="Deploy On Koyeb"></a>
</p>
<h3 align="center">
    ─「 ᴅᴇᴘʟᴏʏᴇʀ ꜱᴜʀ ᴋᴏʏᴇʙ 」─
</h3>
<p align="center"> <a href="https://railway.app/deploy"><img height="45px" src="https://railway.app/button.svg"></a>
</p>
<h3 align="center">
    ─「 ᴅᴇᴘʟᴏʏᴇʀ ꜱᴜʀ ʀᴇɴᴅᴇʀ 」─
</h3>
<p align="center"><a href="https://render.com/deploy">
<img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render"></a>
</p>
<h3 align="center">
    ─「 ᴅᴇᴘʟᴏʏᴇʀ ꜱᴜʀ ᴠᴘꜱ 」─
</h3>
</details>

---

### 1. Cloner le projet

```bash
git clone https://github.com/Sev228/Upload-Metadata-Change-Bot.git
cd Upload-Metadata-Change-Bot
```
---
### 2. Créer un environnement virtuel pour le projet
```bash
python3 -m venv venv
source venv/bin/activate
```
---
### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```
---
### 4. Créer les 2 bots directement depuis [Bot Father](https://telegram.me/BotFather/)
- Un Bot pour recevoir les logs
- Un Bot principal pour l'éxecution du code

---
### 5. Créer votre API ID et API HASH sur [Telegram For Developpers](https://core.telegram.org/api/obtaining_api_id)

---
### 6. Créer une Realtime BD sur Firebase et récuperez les infos nécessaires (URL et Clé JSON)

---
### 7. Configurer les variables d’environnement

Crée un fichier .env en vous inspirant de .env.sample :
```
BOT_TOKEN = TOKEN TELEGRAM DU BOT PRINCIPAL

API_ID = VOTRE API ID TELEGRAM

DEVELOPPER_ID = VOTRE ID TELEGRAM

API_HASH = VOTRE API HASH TELEGRAM

LOG_BOT_TOKEN = TOKEN TELEGRAM DU BOT DE LOG

FIREBASE_URL = URL DE VOTRE PROJET FIREBASE

FIREBASE_KEY = VOTRE CLE D'AUTHENTIFICATION FIREBASE
```
---
## 🚀 Utilisation

Lancer le bot :

```bash
python3 main.py
```
### Puis, dans Telegram :

* Entrer dans le chat du Bot
* Tapez la commande `/start`

<b>Voici les commandes du bot et leurs descriptions : </b>
```

start - 🚀 Lance le bot

set_thumb - 📸 Mets à jour votre miniature

show_thumb - 🖼 Montre votre miniature actuelle

del_thumb - 🗑🖼 Supprime votre miniature actuelle

settings - ⚙️ Montre les paramètres 

help - 🆘 Affiche ce message d'aide

set_caption - 📜 Mets à jour la légende des fichiers qui seront envoyés

set_prefix - ⬅️ Mets à jour le préfixe des fichiers qui seront envoyés

set_suffix - ➡️ Mets à jour le suffixe des fichiers qui seront envoyés

del_caption - 🗑 Supprime la légende actuelle

del_prefix - 🗑 Supprime le préfixe

del_suffix - 🗑 Supprime le suffixe actuel
```
---

## 🗂️ Structure du projet

```
.
├── main.py                  # Point d’entrée du bot
├── config.py                # Configuration globale
├── requirements.txt         # Dépendances Python
├── downloads/               # Fichiers téléchargés
├── .env.sample              # Exemple de config .env
├── globals/                 # Modules utilitaires (DB, messages, etc.)
├── helpers/                 # Commandes, gestion du téléchargement/upload
│   └── downloads/Upload_Download/
│       ├── downloader/      # Téléchargement
│       └── uploader/        # Upload et modification
│   └── commands/            # Commandes utilitaires(/start, /help ...)

```
---
## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

```
1. Forker le projet
2. Créer une branche (`git checkout -b feature/ma-feature`)
3. Commiter vos modifications
4. Ouvrir une Pull Request
```
---
## 📫 Contact
- Email: [sevsmart228@gmail.com](mailto:sevsmart228@gmail.com)
- Telegram: [DM TELEGRAM](https://t.me/AKAZARSIS)
---
## Licence

Ce projet est distribué sous la licence `MIT`.

© 2025 - Sev[404] 

---