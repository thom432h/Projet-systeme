# Get the directory of the running PowerShell script
$scriptDirectory = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
# This line determines the path of the directory where the running PowerShell script is located.

# Execute the parcourir.py script
python3 "$scriptDirectory/parcourir.py"
# This line runs the Python script 'parcourir.py' located in the same directory as the PowerShell script.

# Execute the compare.py script
python3 "$scriptDirectory/compare.py"
# This line also runs the Python script 'compare.py' located in the same directory.