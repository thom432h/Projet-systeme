#!/usr/bin/env python
import os
import re

def parcourir_repertoire(repertoire='data'):
    fichiers_vcf = []
    for racine, dossiers, fichiers in os.walk(repertoire):
        for fichier in fichiers:
            if fichier.endswith(".vcf"):
                chemin_complet = os.path.join(racine, fichier)
                fichiers_vcf.append(chemin_complet)
    return fichiers_vcf

def extraire_identifiant(fichier):
    match = re.match(r"(P\d+)[-.](\d+)", fichier)
    if match:
        return match.groups()
    return None, None

def comparer_et_grouper(fichiers_vcf):
    groupes = {}
    for fichier in fichiers_vcf:
        identifiant, _ = extraire_identifiant(os.path.basename(fichier))
        if identifiant:
            if identifiant not in groupes:
                groupes[identifiant] = []
            groupes[identifiant].append(fichier)
    return groupes

def main():
    # Utiliser parcourir_repertoire pour obtenir tous les fichiers VCF
    fichiers_vcf = parcourir_repertoire()
    print("Fichiers VCF trouvés:", fichiers_vcf)

    # Utiliser comparer_et_grouper pour regrouper les fichiers par échantillon
    groupes = comparer_et_grouper(fichiers_vcf)

    # Afficher les groupes dans un format lisible
    for identifiant, fichiers in groupes.items():
        fichiers_simples = [os.path.basename(fichier) for fichier in fichiers]
        fichiers_joints = ', '.join(fichiers_simples)
        print(f"Échantillon {identifiant} : Réplicats {fichiers_joints}")

if __name__ == "__main__":
    main()