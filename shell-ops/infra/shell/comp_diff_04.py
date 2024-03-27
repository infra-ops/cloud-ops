#!/usr/bin/env python3

import os
import sys

# Define the file paths
file1 = "t1/a1.txt"
file2 = "t2/b1.txt"

# Function to print the content of the last modified file
def print_last_modified_content(files):
    last_modified_file = ""
    mod_time = 0

    # Find the last modified file
    for file in files:
        if os.path.exists(file):
            current_mod_time = os.path.getmtime(file)
            if current_mod_time > mod_time:
                mod_time = current_mod_time
                last_modified_file = file

    # Print the content of the last modified file
    if last_modified_file:
        print(f"Content of the last modified file '{last_modified_file}':")
        with open(last_modified_file, 'r') as f:
            print(f.read())
    else:
        print("No files found.")

# Check if both files exist
if not os.path.exists(file1):
    print(f"File '{file1}' does not exist.")
    sys.exit(1)

if not os.path.exists(file2):
    print(f"File '{file2}' does not exist.")
    sys.exit(1)

# Compare the contents of the files
if file1 == file2:
    print(f"Both files '{file1}' and '{file2}' have the same content.")
else:
    print(f"Files '{file1}' and '{file2}' have different content.")

    # Print content of both files
    print(f"Content of {file1}:")
    with open(file1, 'r') as f:
        print(f.read())
    print(f"\nContent of {file2}:")
    with open(file2, 'r') as f:
        print(f.read())

# Call function to print the content of the last modified file
print_last_modified_content([file1, file2])
