#!/bin/bash

echo "" 
if [ "$(command -v jq)" == "" ]; then
   echo "Requirement JQ Tool not installed"
   echo ""
   exit
fi;
if [ "$(command -v yq)" == "" ]; then
   echo "Requirement YQ Tool not installed"
   echo ""
   exit
fi;

file=".gitlab-cis.yml"

if [ ! -f $file ] && [ -z "$1" ]; then
    echo "File .gitlab-ci.yml not found at current directory, neither informed"
    echo "You can inform the Path of the file as a parameter:"
    echo "    ./analyzer /path/to/.gitlab-ci.yaml"
    echo ""
    exit
fi

if [ ! -f $file ] && [ ! -f $1 ]; then
    echo "File $1 not found"
    echo ""
    exit
fi

stages=$(cat .gitlab-ci.yml | yq . | jq .stages)
totalStages=$(echo $stages | jq length)

echo "*********************************************************"
echo " Total Stages....: $totalStages "
for (( c=0; c<totalStages; c++ ))
do
 st="$(echo $stages | jq -r .[$c])"
 echo "  - $st"
done
echo "*********************************************************"
