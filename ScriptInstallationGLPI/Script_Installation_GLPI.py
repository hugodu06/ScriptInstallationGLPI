#!/usr/bin/env python3


####################
# Script_Installation_GLPI.py
# Auteur : Hugo POSCHEL
# Version : 5
# Dernière mise à jour : 24/04/2022
####################


# Importation des modules Python requis pour l'exécution du script

import configparser
import logging
import pymysql
import requests
import shutil
import subprocess
import sys
import tarfile
import wget


# Mise en place et configuration des options de journalisation (logging)

logging.basicConfig(filename='/var/log/installation-glpi.log', encoding='utf-8', format='%(asctime)s - %(name)s : %(levelname)s > %(message)s', level=logging.DEBUG)
journalisationEvenement = logging.getLogger('Script Installation GLPI')


# Saisie du chemin d'accès au répertoire dans lequel a été copié le répertoire contenant le script d'installation de GLPI ainsi que les autres fichiers de configuration externes

print("Saisir le chemin d'accès au répertoire dans lequel a été copié le répertoire contenant le script d'installation de GLPI ainsi que les autres fichiers de configuration externes")
cheminAccesRepertoireContenantRepertoireScriptInstallationGLPI = input()
cheminAccesFichierDeConfigurationExterneIni = cheminAccesRepertoireContenantRepertoireScriptInstallationGLPI + "/ScriptInstallationGLPI/config.ini"

if cheminAccesRepertoireContenantRepertoireScriptInstallationGLPI == '':
    print("Erreur critique : Attention, il est obligatoire de saisir le chemin d'accès au répertoire dans lequel a été copié le répertoire contenant le script d'installation de GLPI ainsi que les autres fichiers de configuration externes !")
    journalisationEvenement.critical("Le chemin d'accès au répertoire dans lequel a été copié le répertoire contenant le script d'installation de GLPI ainsi que les autres fichiers de configuration externes n'a pas été saisi !")
    sys.exit(10)


# Extraction des données du fichier de configuration externe 'config.ini' et définition des variables nécessaires à l'exécution du script

try:
    fichierDeConfigurationExterneIni = configparser.ConfigParser()
    fichierDeConfigurationExterneIni.read(cheminAccesFichierDeConfigurationExterneIni)
except BaseException as erreur:
    print("Erreur critique : Attention, les données ne peuvent pas être extraites du fichier de configuration externe 'config.ini'. Les variables nécessaires à l'exécution du script ne peuvent donc pas être définies !")
    journalisationEvenement.critical("Les données ne peuvent pas être extraites du fichier de configuration externe 'config.ini' ! >>>" + str(erreur))
    sys.exit(11)

nomHoteMariaDB = fichierDeConfigurationExterneIni['Variables']['nomHoteMariaDB']
nomUtilisateurRootMariaDB = fichierDeConfigurationExterneIni['Variables']['nomUtilisateurRootMariaDB']
motDePasseUtilisateurRootMariaDB = fichierDeConfigurationExterneIni['Mots De Passe']['motDePasseUtilisateurRootMariaDB']
nomBaseDeDonneesGLPIMariaDB = fichierDeConfigurationExterneIni['Variables']['nomBaseDeDonneesGLPIMariaDB']
nomUtilisateurGLPIMariaDB = fichierDeConfigurationExterneIni['Variables']['nomUtilisateurGLPIMariaDB']
motDePasseUtilisateurGLPIMariaDB = fichierDeConfigurationExterneIni['Mots De Passe']['motDePasseUtilisateurGLPIMariaDB']
cheminAccesRepertoireDonneesSystemeFuseauxHoraires = fichierDeConfigurationExterneIni['Variables']['cheminAccesRepertoireDonneesSystemeFuseauxHoraires']
urlListeVersionsGLPI = fichierDeConfigurationExterneIni['Variables']['urlListeVersionsGLPI']
cheminAccesRepertoireDestinationTelechargementVersionGLPIAInstaller = fichierDeConfigurationExterneIni['Variables']['cheminAccesRepertoireDestinationTelechargementVersionGLPIAInstaller']
cheminAccesRepertoireInstallationGLPIServeurWebApache = fichierDeConfigurationExterneIni['Variables']['cheminAccesRepertoireInstallationGLPIServeurWebApache']
cheminAccesRepertoireConfigurationGLPIServeurWebApache = fichierDeConfigurationExterneIni['Variables']['cheminAccesRepertoireConfigurationGLPIServeurWebApache']
langueInstallationGLPI = fichierDeConfigurationExterneIni['Variables']['langueInstallationGLPI']
nomVirtualHostGLPIServeurWebApache = fichierDeConfigurationExterneIni['Variables']['nomVirtualHostGLPIServeurWebApache']
cheminAccesModeleFichierConfigurationVirtualHostGLPIServeurWebApache = fichierDeConfigurationExterneIni['Variables']['cheminAccesModeleFichierConfigurationVirtualHostGLPIServeurWebApache']
cheminAccesFichierConfigurationVirtualHostGLPIServeurWebApache = fichierDeConfigurationExterneIni['Variables']['cheminAccesFichierConfigurationVirtualHostGLPIServeurWebApache']


# Téléchargement et installation des mises à jour des paquets disponibles

subprocess.run(args=["apt-get", "update"])
subprocess.run(args=["apt-get", "dist-upgrade", "-y"])


# Installation des paquets nécessaires à l'installation et à l'utilisation de GLPI

subprocess.run(args=["apt-get", "install", "apache2", "libapache2-mod-php", "-y"])
subprocess.run(args=["apt-get", "install", "php", "php-imap", "php-ldap", "php-curl", "php-xmlrpc", "php-gd", "php-mysql", "php-cas", "php-intl", "php-dom", "php-xml", "php-simplexml", "php-apcu", "php-mbstring", "php-zip", "php-bz2", "-y"])
subprocess.run(args=["apt-get", "install", "apcupsd", "zip", "bzip2", "-y"])
subprocess.run(args=["apt-get", "install", "mariadb-server", "-y"])


# Amélioration de la sécurité de l'installation MariaDB via l'exécution de commandes MySQL, qui équivalent à l'exécution du script 'mariadb-secure-installation'

try:
    commandeModificationMotDePasseUtilisateurRootMariaDB = "mysql -e \"SET PASSWORD FOR \'" + nomUtilisateurRootMariaDB + "\'@\'" + nomHoteMariaDB + "\' = PASSWORD(\'" + motDePasseUtilisateurRootMariaDB + "\')\""
    subprocess.run(args=[commandeModificationMotDePasseUtilisateurRootMariaDB], shell=True)
except BaseException as erreur:
    print("Erreur critique : Attention, le mot de passe de l'utilisateur 'root' du système de gestion des bases de données MariaDB n'a pas pu être modifié correctement !")
    journalisationEvenement.critical("Le mot de passe de l'utilisateur 'root' du système de gestion des bases de données MariaDB n'a pas pu être modifié correctement ! >>>" + str(erreur))
    sys.exit(12)

subprocess.run(args=["systemctl", "restart", "mariadb.service"])

try:
    connexionMariaDB = pymysql.connect(host=nomHoteMariaDB, user=nomUtilisateurRootMariaDB, password=motDePasseUtilisateurRootMariaDB)
    commandeMariaDB = connexionMariaDB.cursor()
    commandeMariaDB.execute("DELETE FROM mysql.user WHERE User='';")
    commandeMariaDB.execute("DELETE FROM mysql.user WHERE User=\'" + nomUtilisateurRootMariaDB + "\' AND Host NOT IN (\'" + nomHoteMariaDB + "\', \'127.0.0.1\', \'::1\');")
    commandeMariaDB.execute("FLUSH PRIVILEGES;")
    connexionMariaDB.close()
except BaseException as erreur:
    print("Erreur : Attention, la sécurité de l'installation MariaDB n'a pas pu être améliorée via l'exécution de commandes MySQL, qui équivalent à l'exécution du script 'mariadb-secure-installation' !")
    journalisationEvenement.error("La sécurité de l'installation MariaDB n'a pas pu être améliorée via l'exécution de commandes MySQL ! >>>" + str(erreur))

subprocess.run(args=["systemctl", "restart", "mariadb.service"])


# Initialisation des données des fuseaux horaires

try:
    commandeInitialisationDonneesFuseauxHoraires = "mysql_tzinfo_to_sql " + cheminAccesRepertoireDonneesSystemeFuseauxHoraires + " | mysql -u " + nomUtilisateurRootMariaDB + " -p" + motDePasseUtilisateurRootMariaDB + " mysql"
    subprocess.run(args=[commandeInitialisationDonneesFuseauxHoraires], shell=True)
except BaseException as erreur:
    print("Avertissement : Attention, les données des fuseaux horaires n'ont pas pu être initialisées correctement !")
    journalisationEvenement.warning("Les données des fuseaux horaires n'ont pas pu être initialisées correctement ! >>>" + str(erreur))

subprocess.run(args=["systemctl", "restart", "mariadb.service"])


# Configuration du système de gestion des bases de données MariaDB

try:
    connexionMariaDB = pymysql.connect(host=nomHoteMariaDB, user=nomUtilisateurRootMariaDB, password=motDePasseUtilisateurRootMariaDB)
    commandeMariaDB = connexionMariaDB.cursor()
    commandeMariaDB.execute("CREATE DATABASE " + nomBaseDeDonneesGLPIMariaDB + ";")
    commandeMariaDB.execute("GRANT ALL PRIVILEGES ON " + nomBaseDeDonneesGLPIMariaDB + ".* TO " + nomUtilisateurGLPIMariaDB + "@" + nomHoteMariaDB + " IDENTIFIED BY \'" + motDePasseUtilisateurGLPIMariaDB + "\';")
    commandeMariaDB.execute("GRANT SELECT ON mysql.time_zone_name TO " + nomUtilisateurGLPIMariaDB + "@" + nomHoteMariaDB + ";")
    commandeMariaDB.execute("FLUSH PRIVILEGES;")
    commandeMariaDB.execute("SHOW DATABASES;")
    listeBasesDeDonneesMariaDB = commandeMariaDB.fetchall()
    for baseDeDonnees in listeBasesDeDonneesMariaDB:
        print(baseDeDonnees)
    connexionMariaDB.close()
except BaseException as erreur:
    print("Erreur critique : Attention, le système de gestion des bases de données MariaDB n'a pas pu être configuré correctement !")
    journalisationEvenement.critical("Le système de gestion des bases de données MariaDB n'a pas pu être configuré correctement ! >>>" + str(erreur))
    sys.exit(13)

subprocess.run(args=["systemctl", "restart", "mariadb.service"])


# Extraction de l'URL de la dernière version stable de GLPI à télécharger et à installer

try:
    reponseURLListeVersionsGLPI = requests.get(urlListeVersionsGLPI)
    reponseJSONURLListeVersionsGLPI = reponseURLListeVersionsGLPI.json()
except BaseException as erreur:
    print("Erreur critique : Attention, les données n'ont pas pu être correctement extraites de la page web au format JSON !")
    journalisationEvenement.critical("Les données n'ont pas pu être correctement extraites de la page web au format JSON ! >>>" + str(erreur))
    sys.exit(14)

numeroCommitVersionGLPIATester = 0
numeroRubriqueCommitVersionGLPIAInstaller = 0

try:
    for commit in reponseJSONURLListeVersionsGLPI:
        versionGLPITesteePreversion = reponseJSONURLListeVersionsGLPI[numeroCommitVersionGLPIATester]["prerelease"]
        if versionGLPITesteePreversion:
            numeroCommitVersionGLPIATester = numeroCommitVersionGLPIATester + 1
        else:
            numeroVersionGLPIAInstaller = reponseJSONURLListeVersionsGLPI[numeroCommitVersionGLPIATester]["name"]
            messageVersionGLPIInstallee = "La version de GLPI qui va être installée est la version "
            messageNumeroVersionGLPIInstallee = messageVersionGLPIInstallee + numeroVersionGLPIAInstaller
            print(messageNumeroVersionGLPIInstallee)
            rubriqueURLTelechargementVersionGLPIAInstaller = reponseJSONURLListeVersionsGLPI[numeroCommitVersionGLPIATester]["assets"]
            urlTelechargementVersionGLPIAInstaller = rubriqueURLTelechargementVersionGLPIAInstaller[numeroRubriqueCommitVersionGLPIAInstaller]["browser_download_url"]
            break
except BaseException as erreur:
    print("Erreur critique : Attention, l'URL de la dernière version stable de GLPI à télécharger et à installer n'a pas pu être extraite correctement de la page web au format JSON !")
    journalisationEvenement.critical("L'URL de la dernière version stable de GLPI n'a pas pu être extraite correctement de la page web au format JSON ! >>>" + str(erreur))
    sys.exit(15)


# Téléchargement du répertoire archivé d'installation de la dernière version stable de GLPI

try:
    nomRepertoireArchiveInstallationGLPITelecharge = wget.download(urlTelechargementVersionGLPIAInstaller, out=cheminAccesRepertoireDestinationTelechargementVersionGLPIAInstaller)
except BaseException as erreur:
    print("Erreur critique : Attention, le répertoire archivé d'installation de la dernière version stable de GLPI n'a pas pu être téléchargé correctement !")
    journalisationEvenement.critical("Le répertoire archivé d'installation de la dernière version stable de GLPI n'a pas pu être téléchargé correctement ! >>>" + str(erreur))
    sys.exit(16)


# Décompression du répertoire archivé d'installation de la dernière version stable de GLPI

try:
    repertoireArchiveInstallationGLPI = tarfile.open(nomRepertoireArchiveInstallationGLPITelecharge, "r:gz")
    repertoireArchiveInstallationGLPI.extractall(cheminAccesRepertoireInstallationGLPIServeurWebApache)
    repertoireArchiveInstallationGLPI.close()
except BaseException as erreur:
    print("Erreur critique : Attention, le répertoire archivé d'installation de la dernière version stable de GLPI n'a pas pu être décompressé correctement !")
    journalisationEvenement.critical("Le répertoire archivé d'installation de la dernière version stable de GLPI n'a pas pu être décompressé correctement ! >>>" + str(erreur))
    sys.exit(17)


# Vérification des prérequis et installation de GLPI

try:
    subprocess.run(args=["php", "bin/console", "glpi:system:check_requirements"], cwd=cheminAccesRepertoireConfigurationGLPIServeurWebApache)
    subprocess.run(args=["php", "bin/console", "db:install", "-L", langueInstallationGLPI, "-H", nomHoteMariaDB, "-d", nomBaseDeDonneesGLPIMariaDB, "-u", nomUtilisateurGLPIMariaDB, "-p", motDePasseUtilisateurGLPIMariaDB, "-n"], cwd=cheminAccesRepertoireConfigurationGLPIServeurWebApache)
except BaseException as erreur:
    print("Erreur critique : Attention, l'installation de GLPI ne s'est pas déroulée correctement !")
    journalisationEvenement.critical("L'installation de GLPI ne s'est pas déroulée correctement ! >>>" + str(erreur))
    sys.exit(18)


# Attribuer (de manière récursive) tous les droits au serveur Web Apache sur le répertoire de configuration de GLPI

try:
    subprocess.run(args=["chown", "-R", "www-data", cheminAccesRepertoireConfigurationGLPIServeurWebApache])
except BaseException as erreur:
    print("Avertissement : Attention, les droits n'ont pas pu être attribués correctement au serveur Web Apache sur le répertoire de configuration de GLPI !")
    journalisationEvenement.warning("Les droits n'ont pas pu être attribués correctement au serveur Web Apache sur le répertoire de configuration de GLPI ! >>>" + str(erreur))

subprocess.run(args=["systemctl", "restart", "apache2.service"])


# Création et activation du VirtualHost de GLPI sur le serveur Web Apache

try:
    fichierConfigurationVirtualHostGLPIServeurWebApache = open(cheminAccesFichierConfigurationVirtualHostGLPIServeurWebApache, "w+")
    fichierConfigurationVirtualHostGLPIServeurWebApache.close()
except BaseException as erreur:
    print("Avertissement : Attention, le fichier de configuration du VirtualHost de GLPI sur le serveur Web Apache n'a pas pu être créé correctement !")
    journalisationEvenement.warning("Le fichier de configuration du VirtualHost de GLPI sur le serveur Web Apache n'a pas pu être créé correctement ! >>>" + str(erreur))

try:
    shutil.copyfile(cheminAccesModeleFichierConfigurationVirtualHostGLPIServeurWebApache,cheminAccesFichierConfigurationVirtualHostGLPIServeurWebApache)
except BaseException as erreur:
    print("Avertissement : Attention, le fichier de configuration du VirtualHost de GLPI sur le serveur Web Apache n'a pas pu être complété correctement à partir du modèle de fichier de configuration fourni !")
    journalisationEvenement.warning("Le fichier de configuration du VirtualHost de GLPI sur le serveur Web Apache n'a pas pu être complété correctement à partir du modèle de fichier de configuration fourni ! >>>" + str(erreur))

try:
    subprocess.run(args=["a2ensite", nomVirtualHostGLPIServeurWebApache])
except BaseException as erreur:
    print("Avertissement : Attention, le VirtualHost de GLPI sur le serveur Web Apache n'a pas pu être activé correctement !")
    journalisationEvenement.warning("Le VirtualHost de GLPI sur le serveur Web Apache n'a pas pu être activé correctement ! >>>" + str(erreur))

subprocess.run(args=["systemctl", "restart", "apache2.service"])

print("Information : Le script d'installation de GLPI s'est exécuté en intégralité, et aucune erreur critique n'est survenue ! GLPI a été correctement installé.")
journalisationEvenement.info("Le script d'installation de GLPI s'est exécuté en intégralité, et aucune erreur critique n'est survenue ! GLPI a été correctement installé.")
sys.exit(0)