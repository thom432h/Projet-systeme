# Obtient le répertoire du script PowerShell en cours d'exécution
$scriptDirectory = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Exécute le script parcourir.py
python3 "$scriptDirectory/parcourir.py"

# Exécute le script compare.py
python3 "$scriptDirectory/compare.py"