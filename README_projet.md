System Project: ReplicatBio

Overview

The ReplicatBio Project is an initiative to automate the comparison of genomic data from DNA sequencing. Focused on the analysis of Herpesvirus3 genomes, the project uses Python and bash scripts to process and analyze VCF files. Its aim is to identify and compare genetic variants among different samples and replicates.

Scripts

parcourir.py:
This script is designed to navigate file systems and organize VCF files. It extracts key information, such as unique identifiers, to group and prepare data for analysis. This script facilitates data management and ensures efficient organization before performing comparative analyses.

compare.py:
This script analyzes VCF files to compare genetic variants. It uses complex data structures, such as dictionaries, to store and efficiently compare sequential information. Its key role is to identify common genetic variants among different samples, which is essential for understanding similarities and differences in sequencing data.

main_powershell.ps1 or main.sh:
This is the main script that orchestrates the entire project workflow. It executes and manages the other Python scripts, ensuring a smooth and coordinated execution of the analysis process. This script plays a crucial role in managing operations and verifying results.

Objectives and Features :
Automate the comparison of VCF files for accurate genomic analysis.
Identify common genetic variants, providing a clear overview of similarity and variation among replicates.
Use efficient and accurate data processing methods to ensure data integrity and reliability of results.

Required Configuration :
Bash environment for executing the scripts.
Python 3, with the os, re, sys modules for data processing and analysis.

Make sure to place the scripts as well as the data in the same directory.

Author: Thomas Vitré
Last Updated: 12/22/2023
