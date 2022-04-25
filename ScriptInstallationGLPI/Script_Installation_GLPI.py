#!/usr/bin/env python3


import configparser
import logging
import pymysql
import requests
import shutil
import subprocess
import sys
import tarfile
import wget




print("Saisir le chemin d'accès au répertoire dans lequel a été copié le répertoire contenant le script d'installation de GLPI ainsi que les autres fichiers de configuration externes")
cheminAccesRepertoireContenantRepertoireScriptInstallationGLPI = input()
cheminAccesFichierDeConfigurationExterneIni = cheminAccesRepertoireContenantRepertoireScriptInstallationGLPI + "/ScriptInstallationGLPI/config.ini"



fichierDeConfigurationExterneIni = configparser.ConfigParser()
fichierDeConfigurationExterneIni.read(cheminAccesFichierDeConfigurationExterneIni)


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





subprocess.run(args=["apt-get", "update"])
subprocess.run(args=["apt-get", "dist-upgrade", "-y"])


subprocess.run(args=["apt-get", "install", "apache2", "libapache2-mod-php", "-y"])
subprocess.run(args=["apt-get", "install", "php", "php-imap", "php-ldap", "php-curl", "php-xmlrpc", "php-gd", "php-mysql", "php-cas", "php-intl", "php-dom", "php-xml", "php-simplexml", "php-apcu", "php-mbstring", "php-zip", "php-bz2", "-y"])
subprocess.run(args=["apt-get", "install", "apcupsd", "zip", "bzip2", "-y"])
subprocess.run(args=["apt-get", "install", "mariadb-server", "-y"])




commandeModificationMotDePasseUtilisateurRootMariaDB = "mysql -e \"SET PASSWORD FOR \'" + nomUtilisateurRootMariaDB + "\'@\'" + nomHoteMariaDB + "\' = PASSWORD(\'" + motDePasseUtilisateurRootMariaDB + "\')\""
subprocess.run(args=[commandeModificationMotDePasseUtilisateurRootMariaDB], shell=True)


subprocess.run(args=["systemctl", "restart", "mariadb.service"])





connexionMariaDB = pymysql.connect(host=nomHoteMariaDB, user=nomUtilisateurRootMariaDB, password=motDePasseUtilisateurRootMariaDB)
commandeMariaDB = connexionMariaDB.cursor()
commandeMariaDB.execute("DELETE FROM mysql.user WHERE User='';")
commandeMariaDB.execute("DELETE FROM mysql.user WHERE User=\'" + nomUtilisateurRootMariaDB + "\' AND Host NOT IN (\'" + nomHoteMariaDB + "\', \'127.0.0.1\', \'::1\');")
commandeMariaDB.execute("FLUSH PRIVILEGES;")
connexionMariaDB.close()


subprocess.run(args=["systemctl", "restart", "mariadb.service"])




commandeInitialisationDonneesFuseauxHoraires = "mysql_tzinfo_to_sql " + cheminAccesRepertoireDonneesSystemeFuseauxHoraires + " | mysql -u " + nomUtilisateurRootMariaDB + " -p" + motDePasseUtilisateurRootMariaDB + " mysql"
subprocess.run(args=[commandeInitialisationDonneesFuseauxHoraires], shell=True)


subprocess.run(args=["systemctl", "restart", "mariadb.service"])