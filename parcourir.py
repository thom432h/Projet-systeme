#!/usr/bin/env python
# Indique que ce script doit être exécuté avec Python.

import os
# Importe le module os pour interagir avec le système de fichiers.

import re
# Importe le module re pour les expressions régulières.

def parcourir_repertoire(repertoire='data'):
    # Définit une fonction pour parcourir un répertoire et trouver des fichiers VCF.

    fichiers_vcf = []
    # Initialise une liste pour stocker les chemins des fichiers VCF.

    for racine, dossiers, fichiers in os.walk(repertoire):
        # Parcourt le répertoire et ses sous-dossiers.

        for fichier in fichiers:
            # Parcourt chaque fichier dans le répertoire courant.

            if fichier.endswith(".vcf"):
                # Vérifie si le fichier a une extension .vcf.

                chemin_complet = os.path.join(racine, fichier)
                # Crée le chemin complet du fichier.

                fichiers_vcf.append(chemin_complet)
                # Ajoute le chemin complet à la liste des fichiers VCF.

    return fichiers_vcf
    # Retourne la liste des chemins de fichiers VCF.

def extraire_identifiant(fichier):
    # Définit une fonction pour extraire l'identifiant d'un fichier.

    match = re.match(r"(P\d+)[-.](\d+)", fichier)
    # Utilise une expression régulière pour extraire l'identifiant.

    if match:
        # Si l'expression régulière trouve une correspondance.

        return match.groups()
        # Retourne les groupes trouvés par l'expression régulière.

    return None, None
    # Retourne None si aucune correspondance n'est trouvée.

def comparer_et_grouper(fichiers_vcf):
    # Définit une fonction pour regrouper les fichiers VCF par identifiant.

    groupes = {}
    # Initialise un dictionnaire pour les groupes.

    for fichier in fichiers_vcf:
        # Parcourt chaque fichier VCF.

        identifiant, _ = extraire_identifiant(os.path.basename(fichier))
        # Extrait l'identifiant du fichier.

        if identifiant:
            # Si un identifiant est trouvé.

            if identifiant not in groupes:
                groupes[identifiant] = []
                # Initialise la liste pour cet identifiant si elle n'existe pas.

            groupes[identifiant].append(fichier)
            # Ajoute le fichier au groupe correspondant.

    return groupes
    # Retourne le dictionnaire des groupes.

def main():
    # Définit la fonction principale.

    fichiers_vcf = parcourir_repertoire()
    # Obtient les fichiers VCF en parcourant le répertoire.

    print("Fichiers VCF trouvés:", fichiers_vcf)
    # Affiche les fichiers VCF trouvés.

    groupes = comparer_et_grouper(fichiers_vcf)
    # Regroupe les fichiers VCF par échantillon.

    for identifiant, fichiers in groupes.items():
        # Parcourt chaque groupe d'identifiant et ses fichiers.

        fichiers_simples = [os.path.basename(fichier) for fichier in fichiers]
        # Crée une liste des noms de fichiers simples.

        fichiers_joints = ', '.join(fichiers_simples)
        # Joint les noms de fichiers en une chaîne.

        print(f"Échantillon {identifiant} : Réplicats {fichiers_joints}")
        # Affiche les identifiants et les fichiers correspondants.

if __name__ == "__main__":
    main()
    # Exécute la fonction main si le script est lancé directement.