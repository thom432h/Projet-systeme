#!/usr/bin/env python
# Cette ligne permet d'exécuter le script avec l'interpréteur Python.

import os
# Importe le module os pour interagir avec le système d'exploitation.

import re
# Importe le module re pour les expressions régulières.

import parcourir
# Importe le module personnalisé parcourir.

def comparer(fichiers, mode='exact'):
    # Définit une fonction pour comparer les variants dans les fichiers VCF.

    dictionnaires = {}
    nb_variants_communs = {}
    # Initialise deux dictionnaires pour stocker les variants et leur nombre.

    for fichier in fichiers:
        # Parcourt chaque fichier dans la liste des fichiers.

        identifiant = re.match(r"(P\d+)[-.]", os.path.basename(fichier)).groups()[0]
        # Extrait l'identifiant de l'échantillon à partir du nom du fichier.

        dictionnaires[identifiant] = {}
        nb_variants_communs[identifiant] = 0
        # Initialise le dictionnaire pour l'identifiant et met à zéro le compteur de variants.

    for fichier in fichiers:
        # Répète le parcours de chaque fichier.

        identifiant = re.match(r"(P\d+)[-.]", os.path.basename(fichier)).groups()[0]
        # Extrait à nouveau l'identifiant de l'échantillon.

        with open(fichier, "r") as f:
            # Ouvre le fichier VCF en mode lecture.

            for ligne in f:
                # Parcourt chaque ligne du fichier.

                if ligne[0] != "#":
                    # Vérifie si la ligne n'est pas un commentaire.

                    chrom, pos, _, _, alt, _, _, _, _, _ = ligne.split('\t')[:10]
                    # Extrait les données de la ligne, en se concentrant sur les colonnes clés.

                    position = int(pos)
                    # Convertit la position en entier.

                    if position not in dictionnaires[identifiant]:
                        dictionnaires[identifiant][position] = set()
                        # Ajoute la position au dictionnaire s'il n'y est pas déjà.

                    dictionnaires[identifiant][position].add(alt)
                    # Ajoute l'alt à la position spécifique dans le dictionnaire.
                        # Comparaison des variants
    for identifiant, variants in dictionnaires.items():
        # Parcourt chaque identifiant et ses variants associés dans le dictionnaire.

        for pos, alts in variants.items():
            # Parcourt chaque position et les altérations correspondantes.

            if mode == 'exact':
                # En mode exact, on compare les altérations de façon stricte.

                if all(alts == variants.get(pos, set()) for idt, variants in dictionnaires.items() if idt != identifiant):
                    # Vérifie si les altérations sont identiques pour tous les identifiants sauf celui en cours.

                    nb_variants_communs[identifiant] += 1
                    # Incrémente le compteur pour l'identifiant si les altérations sont identiques.

            elif mode == 'range':
                # En mode range, on compare les altérations dans un intervalle autour de la position.

                for compare_pos in range(pos - 10, pos + 11):
                    # Crée un intervalle de positions à comparer.

                    if any(compare_pos in variants and alts == variants[compare_pos] for idt, variants in dictionnaires.items() if idt != identifiant):
                        # Vérifie si les altérations sont identiques pour une position dans l'intervalle.

                        nb_variants_communs[identifiant] += 1
                        # Incrémente le compteur si une correspondance est trouvée dans l'intervalle.

                        break
                        # Sort de la boucle si une correspondance est trouvée.

    return nb_variants_communs
    # Retourne le dictionnaire contenant le nombre de variants communs pour chaque identifiant.
def main():
    # Fonction principale qui est exécutée lors du démarrage du script.

    fichiers_vcf = parcourir.parcourir_repertoire()
    # Appelle la fonction parcourir_repertoire du module parcourir pour obtenir la liste des fichiers VCF.

    # Version exacte
    nb_variants_communs_exact = comparer(fichiers_vcf, mode='exact')
    # Appelle la fonction comparer pour obtenir le nombre de variants communs en mode exact.

    print("Nombre total de variants communs (mode exact):")
    for groupe, nb in nb_variants_communs_exact.items():
        # Parcourt le dictionnaire des variants communs et affiche les résultats pour chaque groupe.

        print(f"{groupe}: {nb}")
        # Affiche l'identifiant du groupe et le nombre de variants communs en mode exact.

    # Version range
    nb_variants_communs_range = comparer(fichiers_vcf, mode='range')
    # Appelle la fonction comparer pour obtenir le nombre de variants communs en mode range.

    print("\nNombre total de variants communs (mode range):")
    for groupe, nb in nb_variants_communs_range.items():
        # Parcourt le dictionnaire des variants communs en mode range et affiche les résultats pour chaque groupe.

        print(f"{groupe}: {nb}")
        # Affiche l'identifiant du groupe et le nombre de variants communs en mode range.

if __name__ == "__main__":
    # Vérifie si le script est exécuté en tant que programme principal.

    main()
    # Appelle la fonction main.