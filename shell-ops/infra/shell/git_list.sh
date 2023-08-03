#!/bin/bash

# User or organization name
USER_NAME="nik786"

# Output file name
OUTPUT_FILE="repo_links.txt"

# Get list of repository names
REPO_LIST=$(curl -s "https://api.github.com/users/$USER_NAME/repos?per_page=1000" | grep -oP '"name": "\K([^"]*)')

# Loop through repository names and get clone URLs
for REPO_NAME in $REPO_LIST
do
    REPO_URL=$(git ls-remote --get-url "git://github.com/$USER_NAME/$REPO_NAME.git")
    echo $REPO_URL >> $OUTPUT_FILE
done

echo "Done! All repository links for user $USER_NAME saved to $OUTPUT_FILE."
