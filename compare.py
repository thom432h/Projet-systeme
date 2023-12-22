#!/usr/bin/env python
# This line is used to indicate that this script should be executed using Python, especially on Unix/Linux systems.

import os
# Imports the os module to enable interactions with the computer's file system.

import re
# Imports the re module for using regular expressions, useful for pattern matching in strings.

import parcourir  
# Imports a custom module named 'parcourir'. This module should contain a function to traverse directories and find files.

def create_combinations(replicates):
    # Defines a function to create combinations of replicates. This replaces the functionality of itertools.combinations.
    combos = []  # Initializes an empty list to store combinations.
    for i in range(len(replicates)):  # Loops through each replicate.
        for j in range(i+1, len(replicates)):  # Loops through subsequent replicates to create pairs.
            combos.append((replicates[i], replicates[j]))  # Adds the pair of replicates to the combinations list.
    combos.append(tuple(replicates))  # Also adds a combination of all replicates.
    return combos  # Returns the list of replicate combinations.

def comparer(fichiers, mode='exact'):
    # Defines a function to compare variants in VCF files. Accepts a list of files and a comparison mode ('exact' or 'range').
    dictionaries = {}  # Initializes a dictionary to store variant data.
    for fichier in fichiers:  # Loops through each provided VCF file.
        # Extracts the identifier and replicate number from the file name.
        identifier, replicate = re.match(r"(P\d+)[-.](\d+)", os.path.basename(fichier)).groups()
        # Initializes the dictionary for this identifier and replicate if they do not already exist.
        if identifier not in dictionaries:
            dictionaries[identifier] = {}
        if replicate not in dictionaries[identifier]:
            dictionaries[identifier][replicate] = {}
        # Opens the VCF file and iterates through its lines.
        with open(fichier, "r") as f:
            for line in f:
                if line[0] != "#":  # Ignores comment lines.
                    # Extracts relevant information from the line (chromosome, position, alteration).
                    chrom, pos, _, _, alt, _, _, _, _, _ = line.split('\t')[:10]
                    position = int(pos)  # Converts the position to an integer.
                    # Adds the alteration to the position for this replicate.
                    if position not in dictionaries[identifier][replicate]:
                        dictionaries[identifier][replicate][position] = set()
                    dictionaries[identifier][replicate][position].add(alt)

    common_variants = {idt: {} for idt in dictionaries}  # Initializes a dictionary to count common variants.
    for identifier, replicates in dictionaries.items():
        # Creates combinations of replicates to compare.
        combos = create_combinations(list(replicates.keys()))
        for combo in combos:
            # Counts the number of common variants for each combination.
            count = 0
            # Union of positions of all replicates in the combination to iterate through all possible positions.
            for pos in set().union(*(replicates[rep].keys() for rep in combo)):
                # Retrieves alterations for each replicate at this position.
                alts = [replicates[rep].get(pos, set()) for rep in combo]
                if mode == 'exact':
                    # In 'exact' mode, checks if all alterations are identical at this position.
                    if all(alts[0] == alt for alt in alts[1:]):
                        count += 1
                elif mode == 'range':
                    # In 'range' mode, checks within a range of positions around the current position.
                    for compare_pos in range(pos - 10, pos + 11):
                        # Retrieves alterations for each replicate at the comparison position.
                        alts_range = [replicates[rep].get(compare_pos, set()) for rep in combo]
                        # Checks if all alterations in the range are identical.
                        if all(alts_range) and all(alts_range[0] == alt for alt in alts_range[1:]):
                            count += 1
                            break
            common_variants[identifier][combo] = count  # Stores the number of common variants for this combination.

    return common_variants  # Returns the number of common variants for each combination of replicates per sample.

def main():
    # Main function of the script. Coordinates reading VCF files, comparing them, and displaying results.
    vcf_files = parcourir.parcourir_repertoire()  # Calls the function to get VCF files.
    # Iterates through comparison modes and displays results for each mode.
    for mode in ['exact', 'range']:
        print(f"\nTotal number of common variants (mode {mode}):")
        # Calls the comparison function for the current mode.
        comparisons = comparer(vcf_files, mode)
        # Displays comparison results for each sample identifier.
        for identifier, combos in comparisons.items():
            print(f"{identifier}:")
            for combo, count in combos.items():
                # Formats and displays the results for each combination of replicates.
                replicates = " and ".join(combo)
                print(f"    replicate {replicates} : {count}")

if __name__ == "__main__":
    main()  # Executes the main function if the script is run directly.