#!/usr/bin/env python
import os
import re
import parcourir

def comparer(fichiers, mode='exact'):
    dictionnaires = {}
    nb_variants_communs = {}

    # Initialiser les dictionnaires pour chaque identifiant d'échantillon
    for fichier in fichiers:
        identifiant = re.match(r"(P\d+)[-.]", os.path.basename(fichier)).groups()[0]
        dictionnaires[identifiant] = {}
        nb_variants_communs[identifiant] = 0

    # Remplir les dictionnaires avec les données des fichiers VCF
    for fichier in fichiers:
        identifiant = re.match(r"(P\d+)[-.]", os.path.basename(fichier)).groups()[0]
        with open(fichier, "r") as f:
            for ligne in f:
                if ligne[0] != "#":
                    chrom, pos, _, _, alt, _, _, _, _, _ = ligne.split('\t')[:10]
                    position = int(pos)

                    if position not in dictionnaires[identifiant]:
                        dictionnaires[identifiant][position] = set()
                    dictionnaires[identifiant][position].add(alt)

    # Comparaison des variants
    for identifiant, variants in dictionnaires.items():
        for pos, alts in variants.items():
            if mode == 'exact':
                if all(alts == variants.get(pos, set()) for idt, variants in dictionnaires.items() if idt != identifiant):
                    nb_variants_communs[identifiant] += 1
            elif mode == 'range':
                for compare_pos in range(pos - 10, pos + 11):
                    if any(compare_pos in variants and alts == variants[compare_pos] for idt, variants in dictionnaires.items() if idt != identifiant):
                        nb_variants_communs[identifiant] += 1
                        break

    return nb_variants_communs

def main():
    fichiers_vcf = parcourir.parcourir_repertoire()

    # Version exacte
    nb_variants_communs_exact = comparer(fichiers_vcf, mode='exact')
    print("Nombre total de variants communs (mode exact):")
    for groupe, nb in nb_variants_communs_exact.items():
        print(f"{groupe}: {nb}")

    # Version range
    nb_variants_communs_range = comparer(fichiers_vcf, mode='range')
    print("\nNombre total de variants communs (mode range):")
    for groupe, nb in nb_variants_communs_range.items():
        print(f"{groupe}: {nb}")

if __name__ == "__main__":
    main()