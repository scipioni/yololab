#!/bin/sh

# Replace the first character for each line of a file (and for every file in a directory)
# with 81 if the first character is 0 or with 82 if the first character is 1

# Get the current directory
DIR=$1

# Iterate over all files in the current directory


set -x

cd $DIR

for FILE in *.txt; do

  # Check if the file is a directory
  if [ -d "$FILE" ]; then

    # Recursively call the script on the directory
    echo "Replacing first character in files in directory $FILE..."
    #cd "$file"
    bash replace-first-character.sh $FILE
  else

    # Replace the first character of each line in the file
    echo "Replacing first character in file $FILE..."
    sed -i 's/^0/81/; s/^1/82/' "$FILE"
	break
  fi

done
