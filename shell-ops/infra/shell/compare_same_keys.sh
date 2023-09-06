# Set the delimiter
delimiter="="

# Read the keys from the first file into an array
mapfile -t keys < <(awk -F"$delimiter" '{print $1}' file1)

# Iterate over the keys and compare them with the second file
for key in "${keys[@]}"; do
    # Use grep to check if the key exists in the second file
    if grep -q "$key$delimiter" file2; then
        echo "Key '$key' exists in both files."
    fi
done
