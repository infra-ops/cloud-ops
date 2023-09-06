#!/bin/bash

# Set the delimiter
delimiter="="

# Initialize an array to store keys that do not exist in the second file
not_found=()

# Read and process each line of the first file
while IFS= read -r line; do
    key=$(echo "$line" | awk -F"$delimiter" '{print $1}')
    if grep -q "$key$delimiter" file2; then
        echo "Key '$key' exists in both files."
    fi
done < "file1"


grep -c -vE '^\s*$' file1
wc -l file1


