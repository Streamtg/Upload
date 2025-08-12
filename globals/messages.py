DOWNLOAD_START = "🤖Début du Télechargement de <b>{}</b>...🚀"

PROGRESS = """
⏳ <b>Pourcentage:</b> {0}%
📥 <b>Téléchargé:</b> {1} / {2}
⚡️ <b>Vitesse:</b> {3}/s
🕰 <b>Temps Restant:</b> {4}
"""

DOWNLOAD_FINISHED = "🤖✅Téléchargement terminé!!!, traitement en cours..."

ALREADY_IN_DOWNLOAD = ("🤖Vous êtes déjà en train de télécharger un fichier, veuillez pat"
                       "ienter avant d'en lancer un autre.")

NO_LINK_DETECTED = "❌Aucun lien détecté, veuillez réessayer"

FILE_NOT_FOUND = "❌Fichier non trouvé, veuillez recommencer"

IMPOSSIBLE_DOWNLOAD = "🤖Je ne peux pas télécharger de fichier dépasssant 2Go"

DOWNLOAD_FAILED = "❌Echec lors du téléchargement du fichier : {}"

UPLOAD_FAILED = "❌Echec lors de l'envoi du fichier : {}"

ERROR_OCCURRED = "❗️Une erreur s'est produite : {}"

DETECTING_LINK = "🤖Récupération des informations du lien en cours...⏳"

FILE_UPLOADING = "🤖ᴜᴘʟᴏᴀᴅ ᴇɴ ᴄᴏᴜʀꜱ.."

SEND_THUMBNAIL = "📷 Veuillez envoyer la miniature pour vos prochains Uploads"

THUMBNAIL_SET = "✅Miniature définie avec succès, elle sera utilisée pour vos prochains Uploads"

SEND_THUMBNAIL_TIMEOUT = "⏳Temps écoulé pour envoyer la miniature, veuillez recommencer"

THUMBNAIL_DELETED = "✅Miniature supprimée avec succès, elle ne sera plus utilisée pour vos prochains Uploads"

CURRENT_THUMBNAIL = "📷 Voici la miniature actuellement définie pour vos prochains Uploads"

NO_THUMBNAIL_SET = "❌Aucune miniature définie, veuillez en définir une avec /set_thumb"
ASK_NEW_FILENAME = "📂 Veuillez entrer le nouveau nom du fichier (sans l'extension) :\n\n" \
                    "🪄 <b>Nom actuel du fichier:</b> <code>{}</code>"
SETTINGS = "⚙️ Paramètres de Bot, cliquez sur une option pour afficher l'option\n\n"

REPLY_TO_PHOTO = "❌Veuillez répondre à une photo par cette commande pour la définir comme miniature"

NEW_FILENAME_PLACEHOLDER = "Nouveau nom du fichier (sans l'extension)"

RENAME_TIMEOUT = "Temps écoulé pour renommer le fichier, veuillez recommencer"
FILE_TOO_LARGE = "❌Le fichier est trop volumineux pour être envoyé, la limite est de 2Go"

FILE_UPLOAD_FAILED = "❌Echec lors de l'envoi du fichier"

SET_CAPTION = """<b>Pour définir une légende par défaut, envoyez-la avec la commande</b>:

<u><b>Exemple</b></u>
/set_caption Légende de tous mes fichiers

<b>🔥 Légende avancée</b>
Vous pouvez ajouter différentes variables à la légende, <b>le bot remplacera ces variables par leur valeur</b>

<u><b>Exemple</b></u>
<pre>/set_caption Titre: {filename}
Poids: {filesize}</pre>

La Légende sera donc :
Titre : (Le nom du fichier)
Poids : (Le poids du film)

<b>🕴🏾Variables supportées:</b>

- filename : Répresente le nom du fichier
 
- filesize : Répresente le poids du fichier
 
- duration : Répresente la durée du fichier (Si c'est une vidéo ou un audio)
"""

CAPTION_SET_DONE = "✅Légende mise à jour avec succès"

CAPTION_DELETE = '✅Légende supprimée avec succès'

ABOUT = """™️ A-PROPOS

📝 Langage: <a href='https://www.python.org/'>Python 3</a>

🧰 Framework: <a href='https://github.com/pyrogram/pyrogram'>Pyrogram</a> & <a href='https://github.com/usernein/pyromod'>PyroMod</a>

Blablablablaaaaaaaaaa
"""
INFO_RENAME = "◀️ PRÉFIXE : {}\n\n" \
            "◀️ SUFFIXE : {}\n\n"\
            "💡LEGENDE : {}"

FILE_READY_TO_DOWNLOAD = "📥 Comment voulez uploader ce {} ?\n\n" \
                         "📂 <b>Nom du fichier:</b> <code>{}</code>\n\n" \
                         "📏 <b>Taille du fichier:</b> <code>{}</code>"

HELP = """🤖AIDE

<b>Voici les commandes du bot et leurs descriptions :</b>

/set_thumb - Mets à jour votre miniature</blockquote>

/show_thumb - Montre votre miniature actuelle

/del_thumb - Supprime votre miniatuer actuelle

/settings - Montre les paramètres 

/help - Affiche ce message d'aide

/set_caption - Mets à jour la légende des fichiers qui seront envoyés

/set_prefix - Mets à jour le préfixe des fichiers qui seront envoyés

/set_suffix - Mets à jour le suffixe des fichiers qui seront envoyés

/del_caption - Supprime la légende actuelle

/del_prefix - Supprime le préfixe

/del_suffix - Supprime le suffixe actuel
"""