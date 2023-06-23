#!/bin/bash

toml=$1
force=$3


path=$(dirname $toml)
version=$(toml get --toml-path $toml project.version)
if [ $(find $path -newer $toml | wc -l) = 0 ]; then
  echo "$path $version no upgrade needed"
  [ -n "$force" ] || exit 0
fi

major=0
minor=0
build=0

# break down the version number into it's components
regex="([0-9]+).([0-9]+).([0-9]+)"
if [[ $version =~ $regex ]]; then
  major="${BASH_REMATCH[1]}"
  minor="${BASH_REMATCH[2]}"
  build="${BASH_REMATCH[3]}"
fi

# check paramater to see which number to increment
if [[ "$2" == "feature" ]]; then
  minor=$(echo $minor + 1 | bc)
elif [[ "$2" == "bug" ]]; then
  build=$(echo $build + 1 | bc)
elif [[ "$2" == "major" ]]; then
  major=$(echo $major+1 | bc)
else
  echo "usage: ./version.sh version_number [major/feature/bug]"
  exit -1
fi

# echo the new version number
newversion="${major}.${minor}.${build}"
echo "$path: from $version to $newversion"
toml set --toml-path $toml project.version $newversion


pushd $path
pdm build
twine upload -r galileo dist/*
popd
touch $toml
