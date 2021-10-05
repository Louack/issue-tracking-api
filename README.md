# API Issue Tracking System de SOFTDESK

## DESCRIPTION
L'API permet à des utilisateurs enregistrés de créer des projets pour enregister des problèmes auxquels des commentaires peuvent être ajoutés.

## INSTALLATION

1. Cloner le dépôt du projet avec la commande '$ git clone https://github.com/Louack/OC_PP10.git' ou télécharger le fichier zip du projet à l'adresse 'https://github.com/Louack/OC_PP10/archive/refs/heads/master.zip'
2. Se rendre dans le dossier du projet depuis le terminal de commande
3. Créer un environnement virtuel dans ce dossier avec `$ py -m venv env` sous windows ou bien `$ python3 -m venv env` sous macos ou linux.
4. Activer l'environnement virtuel avec la commande `$ env\Scripts\activate` sous windows ou bien `$ source env/bin/activate` sous macos ou linux.
5. Installer les packages nécessaires au bon fonctionnement du projet avec la commande `$ pip install -r requirements.txt`.
6. Se placer ensuite dans le dossier 'src' et créer et effectuer les migrations vers la base de données grâce à la commande '$ py manage.py makemigrations' suivie de la commande '$ py manage.py migrate'
7. Créer un superutilisateur disposant des droits d'administration avec la commande `$ py manage.py createsuperuser`
8. Enfin lancer le serveur avec la commande `$ py manage.py runserver`. 

## UTILISATION ET FONCTIONNALITES

L'API est accessible depuis l'adresse locale 'http://127.0.0.1:8000/'

La documentation Postman des fonctionnalités est disponible à l'adresse : 
* 'https://www.postman.com/louack/workspace/oc-pp10/documentation/17143964-b737e079-9ddf-4db5-9b6e-560f6d9ab27d'

## BASE DE DONNEES FOURNIE

L'utilisateur 'loic@softdesk.com' dispose des droits d'administration.

Le mot de passe attribué à tous les utilisateurs est : 'api_project'.

Liste des utilisateurs:
* loic@softdesk.com
* roger@softdesk.com
* sylvie@softdesk.com

## GENERATION D'UN RAPPORT FLAKE8

Afin de s'assurer que le programme suit les conventions d'écriture de code PEP 8, un rapport flake8 peut être généré à tout moment dans la console grâce à la commande :

'$ flake8 my_project_folder_path'

Le fichier setup.cfg permet de configurer les préférences d'utilisation du package flake8 :
* max-line-length permet de modifier le nombre de lignes maximum (réglé sur 119 dans le fichier setup d'origine)
* si le répertoire de l'environnement virtuel est présent dans le répertoire du projet, l'exclure (exclude = my_venv_directory)
