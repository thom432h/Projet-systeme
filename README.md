Projet système : RéplicatBio

Vue d'ensemble

Projet RéplicatBio est une initiative pour automatiser la comparaison de données génomiques issues de séquençages d'ADN. 
Focalisé sur l'analyse de génomes Herpesvirus3, 
le projet utilise des scripts en Python et bash ou Powershell pour traiter et analyser des fichiers VCF.
cherchant à identifier et comparer des variants génétiques entre différents échantillons et réplicats.

Scripts

1.parcourir.py
Ce script est conçu pour naviguer dans les fichiers et organiser les fichiers VCF.
Il extrait les informations clés, comme les identifiants uniques, pour regrouper et préparer les données pour l'analyse.
Ce script facilite la gestion des données et assure une organisation efficace avant l'exécution des analyses comparatives.

2. compare.py
Ce script analyse les fichiers VCF pour comparer les variants génétiques.
Il utilise des structures de données complexes, comme des dictionnaires, pour stocker et comparer efficacement les informations séquentielles.
Son rôle clé est d'identifier les variantes génétiques communes entre différents échantillons, ce qui est essentiel pour comprendre les similitudes et les différences dans les données de séquençage.

3.main_powershell.ps1
C'est le script principal qui orchestre l'ensemble du flux de travail du projet. 
Il exécute et gère les autres scripts Python, assurant ainsi une exécution fluide et coordonnée du processus d'analyse. 
Ce script joue un rôle crucial dans la gestion des opérations et la vérification des résultats.

Objectifs et Fonctionnalités

Automatiser la comparaison des fichiers VCF pour une analyse génomique précise.
Identifier les variants génétiques communs, en fournissant un aperçu clair de la similarité et de la variation entre les réplicats.
Utiliser des méthodes de traitement des données efficaces et précises pour assurer l'intégrité et la fiabilité des résultats.

Configuration Requise

Environnement bash ou Powershell pour l'exécution des scripts.
Python 3, avec les modules os, re, sys pour le traitement et l'analyse des données.
