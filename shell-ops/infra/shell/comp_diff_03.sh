#!/bin/bash

# Define the file paths
file1="t1/a1.txt"
file2="t2/b1.txt"

# Function to print the content of the last modified file
print_last_modified_content() {
    files=("$@")
    last_modified_file=""
    mod_time=0

    # Find the last modified file
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            current_mod_time=$(stat -c "%Y" "$file")
            if [ "$current_mod_time" -gt "$mod_time" ]; then
                mod_time=$current_mod_time
                last_modified_file="$file"
            fi
        fi
    done

    # Print the content of the last modified file
    if [ -n "$last_modified_file" ]; then
        echo "Content of the last modified file '$last_modified_file':"
        cat "$last_modified_file"
    else
        echo "No files found."
    fi
}

# Check if both files exist
if [ ! -e "$file1" ]; then
    echo "File '$file1' does not exist."
    exit 1
fi

if [ ! -e "$file2" ]; then
    echo "File '$file2' does not exist."
    exit 1
fi

# Compare the contents of the files
if cmp -s "$file1" "$file2"; then
    echo "Both files '$file1' and '$file2' have the same content."
else
    echo "Files '$file1' and '$file2' have different content."

    # Print content of both files
    echo "Content of $file1:"
    cat "$file1"
    echo ""
    echo "Content of $file2:"
    cat "$file2"
fi

# Call function to print the content of the last modified file
print_last_modified_content "$file1" "$file2"
