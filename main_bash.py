"""
#!/bin/bash
# Affichage du message d'informations
echo "Comparaison des variants pour la version 1..."
python compare.py 1  # Appel du script Python "compare.py" avec l'argument "1" pour la version 1

# Traitement des résultats de la version 1 ici
# Vous pouvez lire les fichiers de sortie de "compare.py" et afficher les résultats.

# Affichage du message d'informations
echo "Comparaison des variants pour la version 2..."
python compare.py 2  # Appel du script Python "compare.py" avec l'argument "2" pour la version 2

# Traitement des résultats de la version 2 ici
# Vous pouvez lire les fichiers de sortie de "compare.py" et afficher les résultats.

# Affichage du message d'informations
echo "Comparaison des variants pour la version 3..."
python compare.py 3  # Appel du script Python "compare.py" avec l'argument "3" pour la version 3

# Traitement des résultats de la version 3 ici
# Vous pouvez lire les fichiers de sortie de "compare.py" et afficher les résultats.
"""
import subprocess

# Fonction pour exécuter la comparaison avec une version donnée
def comparer_version(version):
    print(f"Comparaison des variants pour la version {version}...")
    subprocess.call(["python", "compare.py", str(version)])  # Appel du script Python "compare.py" avec l'argument de la version

    # Traitement des résultats de la version ici
    # Vous pouvez lire les fichiers de sortie de "compare.py" et effectuer le traitement nécessaire.

if __name__ == "__main__":
    versions = [1, 2, 3]

    for version in versions:
        comparer_version(version)