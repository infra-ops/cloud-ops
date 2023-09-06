#!/bin/bash

# Set the delimiter
delimiter="="

# Initialize an array to store keys that do not exist in the second file
not_found=()

# Iterate over the lines of the first file and check if keys exist in the second file
while IFS= read -r line; do
    key=$(echo "$line" | cut -d"$delimiter" -f1)
    if ! grep -q "$key$delimiter" file2; then
        not_found+=("$key")
    fi
done < "file1"

# Check if any keys were not found in the second file
if [ "${#not_found[@]}" -eq 0 ]; then
    echo "All keys from file1 exist in file2."
else
    echo "Keys that do not exist in file2:"
    printf "%s\n" "${not_found[@]}"
fi
