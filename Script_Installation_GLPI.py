#!/usr/bin/env python3

import requests
import wget
import tarfile
import subprocess
import pymysql

subprocess.run(["apt-get", "update"])
subprocess.run(["apt-get", "dist-upgrade"])

subprocess.run(["apt-get", "install", "apache2", "libapache2-mod-php", "-y"])

subprocess.run(["apt-get", "install", "php", "php-imap", "php-ldap", "php-curl", "php-xmlrpc", "php-gd", "php-mysql", "php-cas", "php-intl", "-y"])

subprocess.run(["apt-get", "install", "mariadb-server", "-y"])

subprocess.run(["mysql_secure_installation"])

subprocess.run(["apt-get", "install", "apcupsd", "php-apcu", "-y"])

subprocess.run(["systemctl", "restart", "apache2.service"])
subprocess.run(["systemctl", "restart", "mariadb.service"])

hôtemariadb = "localhost"
utilisateurmariadb = "root"
motdepasseutilisateurmariadb = "Admin2022"

conn = pymysql.connect(host=hôtemariadb, user=utilisateurmariadb, password=motdepasseutilisateurmariadb)
cur = conn.cursor()
cur.execute("create database glpidb")
cur.execute("grant all privileges on glpidb.* to glpiuser@localhost identified by 'Admin2022'")
cur.execute("show databases")
databaseList = cur.fetchall()
for database in databaseList:
    print(database)
conn.close()

subprocess.run(["apt-get", "install", "phpmyadmin", "-y"])

url = "https://api.github.com/repos/glpi-project/glpi/releases?per_page=100"

reponse = requests.get(url)
reponsejson = reponse.json()

numérocommitàtester = 0
numérorubriqueducommitàétudier = 0

for commit in reponsejson:
    versiontestée = reponsejson[numérocommitàtester]["prerelease"]
    if versiontestée:
        numérocommitàtester = numérocommitàtester + 1
    else:
        numeroversioninstallée = reponsejson[numérocommitàtester]["name"]
        messageversioninstallée = "La version de GLPI qui va être installée est la version "
        messageintégralversioninstallée = messageversioninstallée + numeroversioninstallée
        print(messageintégralversioninstallée)
        rubriquelientéléchargement = reponsejson[numérocommitàtester]["assets"]
        liendetéléchargementdelaversion = rubriquelientéléchargement[numérorubriqueducommitàétudier]["browser_download_url"]
        break

répertoiredestinationtéléchargement = "/tmp"
nomarchivetéléchargée = wget.download(liendetéléchargementdelaversion, out=répertoiredestinationtéléchargement)

print("Entrer le chemin d'accès du répertoire dans lequel vous souhaitez installer GLPI sur le serveur Web Apache")
premièrepartiecheminaccèsrépertoireinstallationGLPI = input()

tar = tarfile.open(nomarchivetéléchargée, "r:gz")
tar.extractall(premièrepartiecheminaccèsrépertoireinstallationGLPI)
tar.close()

deuxièmepartiecheminaccèsrépertoireinstallationGLPI = "/glpi"
cheminaccèsrépertoireGLPI = premièrepartiecheminaccèsrépertoireinstallationGLPI + deuxièmepartiecheminaccèsrépertoireinstallationGLPI

subprocess.run(args=["php", "bin/console", "glpi:system:check_requirements"], cwd=cheminaccèsrépertoireGLPI)

subprocess.run(args=["php", "bin/console", "db:install", "-L", "fr_FR", "-H", "localhost", "-d", "glpidb", "-u", "glpiuser", "-p", "Admin2022", "-n"], cwd=cheminaccèsrépertoireGLPI)

subprocess.run(["chown", "-R", "www-data", cheminaccèsrépertoireGLPI])