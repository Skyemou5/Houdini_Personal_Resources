#!/bin/bash

### Initialize env vars for repo and main sub directories
#HOU_PACKAGE
#HOU_HDA
#HOU_BENS_REPO

#MAYBE SET HOUDINI ENV VARS?

#SETUP

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

cd "$parent_path"

env | grep HOU



### get folders
#HDA=./HDA
#PACKAGES=./packages
#PYTOOLS=./python_tools



if [[ -z "${HOU_PACKAGE}" ]]; then
  HOU_PACKAGE="$parent_path/packages"
else
  HOU_PACKAGE="${HOU_PACKAGE}"
fi


if [[ -z "${HOU_HDA}" ]]; then
  HOU_HDA="$parent_path/HDA"
else
  HOU_HDA="${HOU_HDA}"
fi

if [[ -z "${HOU_PYTOOLS}" ]]; then
  HOU_PYTOOLS="$parent_path/python_tools"
else
  HOU_PYTOOLS="${HOU_PYTOOLS}"
fi






c=0
PATHLIST=()
for file in $( ls ); do
    PATHLIST +=  eval "var$c=$file";
    c=$((c+1);
    echo c
done

echo PATHLIST





### set up env vars


### set up houdini vars



### set up simlinks
