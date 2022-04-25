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