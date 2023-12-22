#!/usr/bin/env python
# This line indicates that this script is to be executed with Python.

import os
# Imports the os module to interact with the file system.

import re
# Imports the re module for regular expressions.

def parcourir_repertoire(directory='data'):
    """
    Defines a function to traverse a directory and find VCF files.
    """

    vcf_files = []
    # Initializes a list to store the paths of VCF files.

    for root, dirs, files in os.walk(directory):
        # Traverses the directory and its subdirectories.

        for file in files:
            # Goes through each file in the current directory.

            if file.endswith(".vcf"):
                # Checks if the file has a .vcf extension.

                full_path = os.path.join(root, file)
                # Creates the full path of the file.

                vcf_files.append(full_path)
                # Adds the full path to the list of VCF files.

    return vcf_files
    # Returns the list of VCF file paths.

def extract_identifier(file):
    """
    Defines a function to extract the identifier of a file.
    """

    match = re.match(r"(P\d+)[-.](\d+)", file)
    # Uses a regular expression to extract the identifier.

    if match:
        # If the regular expression finds a match.

        return match.groups()
        # Returns the groups found by the regular expression.

    return None, None
    # Returns None if no match is found.

def compare_and_group(vcf_files):
    """
    Defines a function to group VCF files by identifier.
    """

    groups = {}
    # Initializes a dictionary for the groups.

    for file in vcf_files:
        # Goes through each VCF file.

        identifier, _ = extract_identifier(os.path.basename(file))
        # Extracts the identifier of the file.

        if identifier:
            # If an identifier is found.

            if identifier not in groups:
                groups[identifier] = []
                # Initializes the list for this identifier if it does not exist.

            groups[identifier].append(file)
            # Adds the file to the corresponding group.

    return groups
    # Returns the dictionary of groups.

def main():
    """
    Defines the main function.
    """

    vcf_files = parcourir_repertoire()
    # Obtains the VCF files by traversing the directory.

    print("VCF files found:", vcf_files)
    # Displays the found VCF files.

    groups = compare_and_group(vcf_files)
    # Groups the VCF files by sample.

    print(f"Number of samples: {len(groups)}")
    # Displays the total number of samples.

    for identifier, files in groups.items():
        # Goes through each identifier group and its files.

        simple_files = [os.path.basename(file) for file in files]
        # Creates a list of simple file names.

        print(f"Sample {identifier}: Number of replicates {len(files)}")
        # Displays the identifier and the number of replicates.

        joined_files = ', '.join(simple_files)
        # Joins the file names into a string.

        print(f"Sample {identifier}: Replicates {joined_files}")
        # Displays the identifiers and the corresponding files.

if __name__ == "__main__":
    main()
    # Executes the main function if the script is run directly.