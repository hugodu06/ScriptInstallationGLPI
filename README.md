# Script d'installation de la dernière version stable disponible du logiciel GLPI (*Gestionnaire Libre de Parc Informatique*)

Dépôt GitHub : ***hugodu06/ScriptInstallationGLPI***

Auteur : Hugo POSCHEL

Licence : GNU Affero General Public License v3.0 (AGPL-3.0 License)

----------

## Description du projet *ScriptInstallationGLPI*

Le répertoire *'/ScriptInstallationGLPI'* contient les fichiers suivants :

- *'Script_Installation_GLPI.py'*  
Il s'agit du script qui va permettre l'installation de la dernière version stable disponible du logiciel GLPI.  
Ce script a été rédigé en langage de programmation **Python** en version **3**.  
Ce script permet successivement de :

    - Importer les modules Python requis pour l'exécution du script.
    - Mettre en place et configurer les options de journalisation.
    - Récupérer le chemin d'accès au fichier de configuration externe *'config.ini'*.
    - Extraire les données du fichier de configuration externe *'config.ini'*.
    - Définir les variables nécessaires à l'exécution du script.
    - Télécharger et installer les mises à jour des paquets disponibles.
    - Installer les paquets nécessaires à l'installation et à l'utilisation de GLPI.
    - Modifier le mot de passe de l'utilisateur *'root'* du système de gestion des bases de données MariaDB.
    - Améliorer la sécurité de l'installation MariaDB via l'exécution de commandes MySQL, qui équivalent à l'exécution du script `mariadb-secure-installation`.
    - Initialiser les données des fuseaux horaires.
    - Configurer le système de gestion des bases de données MariaDB.
    - Extraire l'URL de la dernière version stable de GLPI à télécharger et à installer.
    - Télécharger le répertoire archivé d'installation de la dernière version stable de GLPI.
    - Décompresser le répertoire archivé d'installation de la dernière version stable de GLPI.
    - Vérifier les prérequis à l'installation de GLPI.
    - Installer GLPI.
    - Attribuer au serveur Web Apache tous les droits (de manière récursive) sur le répertoire de configuration de GLPI.
    - Créer et activer le VirtualHost de GLPI sur le serveur Web Apache.

- *'config.ini.template'*  
Il s'agit du modèle de fichier de configuration externe *'config.ini'*, qui contient les mots de passe et les variables nécessaires à l'exécution du script. Le script fait appel, lors de son exécution, à ce fichier de configuration externe, pour en extraire les données, afin de définir les variables nécessaires à l'exécution du script.  
Ce fichier de configuration externe a été rédigé au format de données **INI**.

- *'glpi.local.conf'*  
Il s'agit du fichier de configuration externe du VirtualHost de GLPI (*glpi.local*) sur le serveur Web Apache, qui contient les données de configuration du VirtualHost de GLPI. Le script fait appel, lors de son exécution, à ce fichier de configuration externe, pour en extraire les données, afin de créer le fichier de configuration du VirtualHost de GLPI en local sur le serveur Web Apache.

----------

## Environnement d'utilisation du projet *ScriptInstallationGLPI*

Le script d'installation de la dernière version stable disponible du logiciel GLPI doit être exécuté sur un serveur qui tourne sous le système d'exploitation Debian. Il peut également être adapté, en ajustant quelques paramètres, pour pouvoir être exécuté sur un serveur qui tourne sous n'importe quel système d'exploitation dérivé de GNU/Linux.

Le système d'exploitation Debian doit être installé sur le serveur avec au minimum les utilitaires usuels du système. Il est également préférable d'installer un serveur SSH, si l'on souhaite pouvoir accéder à la machine à distance, c'est-à-dire sans y avoir accès physiquement.

L'interface réseau du serveur doit être configurée en statique :

> *En tant que superutilisateur - root*  
> `nano /etc/network/interfaces`

> `allow-hotplug eth0`  
> `iface eth0 inet static`  
> `address 192.168.x.x`  
> `netmask 255.255.255.0`  
> `gateway 192.168.x.x`

Redémarrer le service *networking*, afin de prendre en compte la nouvelle configuration statique de l'interface réseau du serveur :

> *En tant que superutilisateur - root*  
> `service networking restart`

Installer les paquets nécessaires à l'exécution du script :

> *En tant que superutilisateur - root*  
> `apt-get install python3 -y`  
> `apt-get install pip -y`

Installer les modules Python nécessaires à l'exécution du script :

> *En tant que superutilisateur - root*  
> `pip install configparser`  
> `pip install logging`  
> `pip install pymysql`  
> `pip install requests`  
> `pip install shutil`  
> `pip install subprocess`  
> `pip install sys`  
> `pip install tarfile`  
> `pip install wget`

----------

## Mode d'emploi du projet *ScriptInstallationGLPI*

Télécharger le répertoire *'/ScriptInstallationGLPI'* (contenant le script ainsi que les fichiers de configuration externes) dans le répertoire *'/tmp'* du serveur Debian sur lequel le logiciel GLPI doit être installé.

Supprimer l'extension *'.template'* du modèle de fichier de configuration externe *'config.ini.template'*.  
Le fichier doit donc être renommé *'config.ini'* :

> *En tant que superutilisateur - root*  
> `mv /tmp/ScriptInstallationGLPI/config.ini.template /tmp/ScriptInstallationGLPI/config.ini`

Au sein du fichier *'config.ini'*, dans la rubrique *'[Mots De Passe]'*, modifier les valeurs des variables, afin de renseigner les mots de passe désirés pour les utilisateurs *root* et *GLPI* de MariaDB :

> *En tant que superutilisateur - root*  
> `nano /tmp/ScriptInstallationGLPI/config.ini`

> `motDePasseUtilisateurRootMariaDB = xxxxxxxxxx`  
> `motDePasseUtilisateurGLPIMariaDB = xxxxxxxxxx`

Au sein du fichier *'config.ini'*, dans la rubrique *'[Variables]'*, **SI BESOIN** il est également possible de modifier les valeurs de certaines variables, afin d'adapter les paramètres d'installation du logiciel GLPI. Il est notamment possible de modifier les valeurs des variables suivantes :

- Le nom de la base de données de GLPI dans MariaDB
- Le nom de l'utilisateur GLPI dans MariaDB
- Le chemin d'accès au répertoire de destination du téléchargement de la version de GLPI à installer
- Le chemin d'accès au répertoire d'installation de GLPI sur le serveur Web Apache
- Le chemin d'accès au répertoire de configuration de GLPI sur le serveur Web Apache
- La langue d'installation de GLPI
- Le chemin d'accès au modèle du fichier de configuration du VirtualHost de GLPI sur le serveur Web Apache

Au sein du fichier *'glpi.local.conf'*, **SI BESOIN** il faut modifier la valeur de *'DocumentRoot'*, si la valeur de la variable correspondant au chemin d'accès au répertoire de configuration de GLPI sur le serveur Web Apache a été modifiée (et donc par implication, si la valeur de la variable correspondant au chemin d'accès au répertoire d'installation de GLPI sur le serveur Web Apache a été modifiée également).  
La valeur de *'DocumentRoot'* doit donc être égale à la valeur de la variable *'cheminAccesRepertoireConfigurationGLPIServeurWebApache'*.

Exécuter le script d'installation de la dernière version stable disponible du logiciel GLPI

> *En tant que superutilisateur - root*  
> `python3 /tmp/ScriptInstallationGLPI/Script_Installation_GLPI.py`

Lorsque le script le nécessite, saisir le chemin d'accès au répertoire dans lequel a été téléchargé le répertoire *'/ScriptInstallationGLPI'* (contenant le script ainsi que les fichiers de configuration externes).  
Dans le cas où les paramètres d'installation du logiciel GLPI n'ont pas été modifiés, il s'agit du répertoire *'/tmp'*.

> `/tmp`

Laisser le script s'exécuter jusqu'à son terme.

Consulter le fichier de journalisation des évènements survenus au cours de l'exécution du script, afin de déceler d'éventuelles erreurs qui auraient pu survenir au cours de l'installation du logiciel GLPI :

> `cat /var/log/installation-glpi.log`

Mettre à jour les enregistrements DNS sur le serveur DNS du réseau local, afin de faire correspondre l'URL du VirtualHost de GLPI avec l'adresse IP du serveur Web Apache qui l'héberge.