# Script en langage Python d'installation de la dernière version stable de GLPI

Auteur : Hugo POSCHEL

dépot : ScriptInstallationGLPI


## Description du projet

Le répertoire *'ScriptInstallationGLPI'* contient les fichiers suivants :

- *Script_Installation_GLPI.py* : Il s'agit du script rédigé en langage Python qui va permettre l'installation de GLPI.

- *config.ini.template* : Il s'agit du modèle de fichier de configuration au format INI qui contient les mots de passe et les variables nécessaires à l'exécution du script.

- *glpi.local.conf* : Il s'agit du fichier de configuration du VirtualHost de GLPI (*glpi.local*) sur le serveur Web Apache


## Environnement d'utilisation

Le script fonctionne sur un serveur Debian. Il peut cependant être adapté en ajustant quelques paramètres pour fonctionner sur un serveur sous GNU/Linux.

Sur ce serveur Debian doivent avoir été installés python3, pip et les différents modules nécessaires à l'exécution du script.


## Mode d'emploi

Télécharger le répertoire *'ScriptInstallationGLPI'* (conteannt le script et le fichiers de configuration externes) dans le répertoire *'/tmp'* du serveur Debian sur lequel GLPI doit être installé.

supprimer l'extension *'.template'* du modèle de fichier de configuration *'config.ini.template'*
Le fichier doit donc être renommé *'config.ini'*
Modifier les valeurs des variables dans la rubrique *'[Mots De Passe]'*, afin de renseigner les mots de passe désirés pour les utilisateurs root et glpi de mariadb.

exécuter le script en entrant la commande suivante : python3 /tmp/ScriptInstallationGLPI/Script_Installation_GLPI.py

saisir lorsqu'invité /tmp

laisser le script s'exécuter

suivre l'affichage du script pour surveiller les éventuelles erreurs qui pourraient survenir.

Consulter les logs du script pour voir si des erreurs sont survenue : /var/log/installation-glpi.log