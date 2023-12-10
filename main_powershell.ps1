# Obtient le répertoire du script PowerShell en cours d'exécution
$scriptDirectory = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
# Cette ligne détermine le chemin du répertoire où se trouve le script PowerShell en cours d'exécution.

# Exécute le script parcourir.py
python3 "$scriptDirectory/parcourir.py"
# Cette ligne exécute le script Python 'parcourir.py' situé dans le même répertoire que le script PowerShell.

# Exécute le script compare.py
python3 "$scriptDirectory/compare.py"
# Cette ligne exécute le script Python 'compare.py' situé également dans le même répertoire.