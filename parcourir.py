
import os  # Importation du module os pour manipuler les fichiers et les répertoires
import re  # Importation du module re pour effectuer des opérations de correspondance avec des expressions régulières

# Fonction pour lister les réplicats dans un dossier donné
def lister_replicats(chemin_dossier):
    replicats = {}  # Création d'un dictionnaire vide pour stocker les réplicats
    for fichier in os.listdir(chemin_dossier):  # Parcours des fichiers dans le dossier spécifié
        if fichier.endswith('.vcf'):  # Vérification si le fichier se termine par l'extension '.vcf'
            match = re.match(r'P(\d+)-(\d+).trimed1000.sv_sniffles.vcf', fichier)  # Utilisation d'une expression régulière pour extraire des informations du nom de fichier
            if match:  # Vérification si l'expression régulière a trouvé une correspondance dans le nom du fichier
                echantillon = match.group(1)  # Récupération du premier groupe correspondant (numéro de l'échantillon)
                replicat = match.group(2)  # Récupération du deuxième groupe correspondant (numéro du réplicat)
                if echantillon in replicats:  # Vérification si l'échantillon existe déjà dans le dictionnaire replicats
                    replicats[echantillon].append(replicat)  # Ajout du réplicat à la liste existante pour cet échantillon
                else:
                    replicats[echantillon] = [replicat]  # Création d'une nouvelle liste de réplicats pour cet échantillon
    return replicats  # Retourne le dictionnaire contenant les réplicats

if __name__ == "__main__":
    # Chemins des dossiers VCF
    chemin_dossier_vcf_p15 = 'C:\\Users\\Vitre\\Desktop\\Projet systeme\\data\\P15'  # Chemin vers le dossier des fichiers VCF pour P15
    chemin_dossier_vcf_p30 = 'C:\\Users\\Vitre\\Desktop\\Projet systeme\\data\\P30'  # Chemin vers le dossier des fichiers VCF pour P30

    # Lister les réplicats pour chaque échantillon
    replicats_p15 = lister_replicats(chemin_dossier_vcf_p15)  # Appel de la fonction lister_replicats pour P15
    replicats_p30 = lister_replicats(chemin_dossier_vcf_p30)  # Appel de la fonction lister_replicats pour P30

    print("Réplicats P15:", replicats_p15)  # Affichage des réplicats pour P15
    print("Réplicats P30:", replicats_p30)  # Affichage des réplicats pour P30