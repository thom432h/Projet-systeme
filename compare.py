#!/usr/bin/env python
# La ligne ci-dessus est utilisée pour indiquer que ce script est exécuté avec Python, principalement sur les systèmes Unix/Linux.

import os
# Importe le module os pour permettre des interactions avec le système de fichiers de l'ordinateur.

import re
# Importe le module re pour permettre l'utilisation des expressions régulières, utilisées pour la correspondance de motifs dans les chaînes.

import parcourir  
# Importe un module personnalisé nommé 'parcourir'. Ce module doit contenir une fonction pour parcourir les répertoires et trouver des fichiers.

def create_combinations(replicats):
    # Définit une fonction pour créer des combinaisons de réplicats. Cela remplace la fonctionnalité de itertools.combinations.
    combos = []  # Initialise une liste vide pour stocker les combinaisons.
    for i in range(len(replicats)):  # Boucle à travers chaque réplicat.
        for j in range(i+1, len(replicats)):  # Boucle à travers les réplicats suivants pour créer des paires.
            combos.append((replicats[i], replicats[j]))  # Ajoute la paire de réplicats à la liste des combinaisons.
    combos.append(tuple(replicats))  # Ajoute également une combinaison de tous les réplicats.
    return combos  # Retourne la liste des combinaisons de réplicats.

def comparer(fichiers, mode='exact'):
    # Définit une fonction pour comparer les variants dans les fichiers VCF. Accepte une liste de fichiers et un mode de comparaison ('exact' ou 'range').
    dictionnaires = {}  # Initialise un dictionnaire pour stocker les données des variants.
    for fichier in fichiers:  # Parcourt chaque fichier VCF fourni.
        # Extrait l'identifiant et le numéro de réplicat du nom de fichier.
        identifiant, replicat = re.match(r"(P\d+)[-.](\d+)", os.path.basename(fichier)).groups()
        # Initialise le dictionnaire pour cet identifiant et réplicat s'ils n'existent pas déjà.
        if identifiant not in dictionnaires:
            dictionnaires[identifiant] = {}
        if replicat not in dictionnaires[identifiant]:
            dictionnaires[identifiant][replicat] = {}
        # Ouvre le fichier VCF et parcourt ses lignes.
        with open(fichier, "r") as f:
            for ligne in f:
                if ligne[0] != "#":  # Ignore les lignes de commentaires.
                    # Extrait les informations pertinentes de la ligne (chromosome, position, altération).
                    chrom, pos, _, _, alt, _, _, _, _, _ = ligne.split('\t')[:10]
                    position = int(pos)  # Convertit la position en entier.
                    # Ajoute l'altération à la position pour ce réplicat.
                    if position not in dictionnaires[identifiant][replicat]:
                        dictionnaires[identifiant][replicat][position] = set()
                    dictionnaires[identifiant][replicat][position].add(alt)

    nb_variants_communs = {idt: {} for idt in dictionnaires}  # Initialise un dictionnaire pour compter les variants communs.
    for identifiant, replicats in dictionnaires.items():
        # Crée des combinaisons de réplicats à comparer.
        combos = create_combinations(list(replicats.keys()))
        for combo in combos:
            # Compte le nombre de variants communs pour chaque combinaison.
            count = 0
            # Union des positions de tous les réplicats dans la combinaison pour parcourir toutes les positions possibles.
            for pos in set().union(*(replicats[rep].keys() for rep in combo)):
                # Récupère les altérations pour chaque réplicat à cette position.
                alts = [replicats[rep].get(pos, set()) for rep in combo]
                if mode == 'exact':
                    # En mode exact, vérifie si toutes les altérations sont identiques à cette position.
                    if all(alts[0] == alt for alt in alts[1:]):
                        count += 1
                elif mode == 'range':
                    # En mode range, vérifie dans un intervalle de positions autour de la position actuelle.
                    for compare_pos in range(pos - 10, pos + 11):
                        # Récupère les altérations pour chaque réplicat à la position de comparaison.
                        alts_range = [replicats[rep].get(compare_pos, set()) for rep in combo]
                        # Vérifie si toutes les altérations dans l'intervalle sont identiques.
                        if all(alts_range) and all(alts_range[0] == alt for alt in alts_range[1:]):
                            count += 1
                            break
            nb_variants_communs[identifiant][combo] = count  # Stocke le nombre de variants communs pour cette combinaison.

    return nb_variants_communs  # Retourne le nombre de variants communs pour chaque combinaison de réplicats par échantillon.

def main():
    # Fonction principale du script. Coordonne la lecture des fichiers VCF, leur comparaison, et affiche les résultats.
    fichiers_vcf = parcourir.parcourir_repertoire()  # Appelle la fonction pour obtenir les fichiers VCF.
    # Parcourt les modes de comparaison et affiche les résultats pour chaque mode.
    for mode in ['exact', 'range']:
        print(f"\nNombre total de variants communs (mode {mode}):")
        # Appelle la fonction de comparaison pour le mode actuel.
        comparaisons = comparer(fichiers_vcf, mode)
        # Affiche les résultats de comparaison pour chaque identifiant d'échantillon.
        for identifiant, combos in comparaisons.items():
            print(f"{identifiant}:")
            for combo, count in combos.items():
                # Formatte et affiche les résultats pour chaque combinaison de réplicats.
                replicats = " et ".join(combo)
                print(f"    replicat {replicats} : {count}")

if __name__ == "__main__":
    main()  # Exécute la fonction main si le script est lancé directement.