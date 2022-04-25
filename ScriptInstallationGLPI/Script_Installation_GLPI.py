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