#!/bin/sh

# Replace the first character for each line of a file (and for every file in a directory)
# with 81 if the first character is 0 or with 82 if the first character is 1

# Get the current directory
dir=$(pwd)

# Iterate over all files in the current directory

for file in *.txt; do

  # Check if the file is a directory
  if [ -d "$file" ]; then

    # Recursively call the script on the directory
    echo "Replacing first character in files in directory $file..."
    cd "$file"
    bash replace-first-character.sh
    cd "$dir"

  else

    # Replace the first character of each line in the file
    echo "Replacing first character in file $file..."
    sed -i 's/^0/82/g; s/^1/81/g' "$file"

  fi

done