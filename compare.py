import sys  # Importation du module sys pour accéder aux arguments en ligne de commande
import os  # Importation du module os pour manipuler les fichiers et les répertoires
from parcourir import lister_replicats  # Importation de la fonction lister_replicats depuis le module parcourir

# Fonction pour lire un fichier VCF et extraire les variants
def lire_vcf(fichier_vcf):
    variants = {}  # Création d'un dictionnaire vide pour stocker les variants
    with open(fichier_vcf, 'r') as file:  # Ouverture du fichier VCF en mode lecture
        for line in file:  # Parcours des lignes du fichier
            if line.startswith('#'):  # Ignorer les lignes commençant par '#' (commentaires dans le fichier VCF)
                continue
            else:
                elements = line.strip().split('\t')  # Séparation des éléments de la ligne par tabulation
                position = elements[1]  # La position du variant est à l'indice 1
                sequence = elements[4]  # La séquence du variant est à l'indice 4
                if position not in variants:  # Vérification si la position existe déjà dans le dictionnaire variants
                    variants[position] = set()  # Création d'un ensemble vide pour stocker les séquences pour cette position
                variants[position].add(sequence)  # Ajout de la séquence à l'ensemble correspondant à la position
    return variants  # Retourne le dictionnaire contenant les variants

# Fonction pour comparer les variants exacts entre deux jeux de variants
def comparer_variants_exact(variants_replicat1, variants_replicat2):
    communs = 0  # Compteur pour les variants communs
    for position, sequences in variants_replicat1.items():  # Parcours des positions et séquences du premier jeu de variants
        if position in variants_replicat2:  # Vérification si la position existe également dans le deuxième jeu de variants
            communs += len(sequences.intersection(variants_replicat2[position]))  # Calcul de l'intersection des séquences et mise à jour du compteur
    return communs  # Retourne le nombre de variants communs

# Fonction pour comparer les variants par position
def comparer_variants_position(variants_replicat1, variants_replicat2):
    communs = 0  # Compteur pour les variants communs
    for position1, sequences1 in variants_replicat1.items():  # Parcours des positions et séquences du premier jeu de variants
        for position2, sequences2 in variants_replicat2.items():  # Parcours des positions et séquences du deuxième jeu de variants
            if abs(int(position1) - int(position2)) <= 10:  # Vérification si la différence entre les positions est inférieure ou égale à 10
                communs += len(sequences1.intersection(sequences2))  # Calcul de l'intersection des séquences et mise à jour du compteur
    return communs  # Retourne le nombre de variants communs

# Fonction pour comparer les variants par similarité (cette fonction doit être implémentée)
def comparer_variants_similarite(variants_replicat1, variants_replicat2):
    communs = 0  # Compteur pour les variants communs
    # La logique pour comparer la similitude des séquences doit être implémentée ici
    # ...
    return communs  # Retourne le nombre de variants communs

# Fonction pour comparer tous les réplicats dans un dossier donné
def comparer_tous_les_replicats(chemin_dossier, version):
    replicats = lister_replicats(chemin_dossier)  # Appel de la fonction lister_replicats pour obtenir les réplicats dans le dossier spécifié
    for echantillon in replicats:  # Parcours des échantillons dans le dossier
        total_communs = 0  # Compteur pour les variants communs pour un échantillon donné
        for i in range(len(replicats[echantillon])):  # Parcours des réplicats pour un échantillon
            for j in range(i + 1, len(replicats[echantillon])):  # Comparaison avec les réplicats restants
                fichier_vcf1 = os.path.join(chemin_dossier, f'P{echantillon}-{replicats[echantillon][i]}.trimed1000.sv_sniffles.vcf')
                fichier_vcf2 = os.path.join(chemin_dossier, f'P{echantillon}-{replicats[echantillon][j]}.trimed1000.sv_sniffles.vcf')

                variants_replicat1 = lire_vcf(fichier_vcf1)  # Extraction des variants du premier réplicat
                variants_replicat2 = lire_vcf(fichier_vcf2)  # Extraction des variants du deuxième réplicat

                if version == "1":
                    total_communs += comparer_variants_exact(variants_replicat1, variants_replicat2)  # Comparaison exacte
                elif version == "2":
                    total_communs += comparer_variants_position(variants_replicat1, variants_replicat2)  # Comparaison par position
                elif version == "3":
                    total_communs += comparer_variants_similarite(variants_replicat1, variants_replicat2)  # Comparaison par similarité

        print(f"Total de variants communs pour l'échantillon P{echantillon} (Version {version}): {total_communs}")  # Affichage du nombre de variants communs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compare.py [version]")
        sys.exit(1)

    version = sys.argv[1]  # Récupération de la version depuis les arguments en ligne de commande
    chemin_dossier_vcf_p15 = 'C:\\Users\\Vitre\\Desktop\\Projet systeme\\data\\P15'  # Chemin vers le dossier des fichiers VCF pour P15
    chemin_dossier_vcf_p30 = 'C:\\Users\\Vitre\\Desktop\\Projet systeme\\data\\P30'  # Chemin vers le dossier des fichiers VCF pour P30

    comparer_tous_les_replicats(chemin_dossier_vcf_p15, version)  # Comparaison des réplicats pour P15 avec la version spécifiée
    comparer_tous_les_replicats(chemin_dossier_vcf_p30, version)  # Comparaison des réplicats pour P30 avec la version spécifiée