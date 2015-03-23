#!/bin/bash

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

project="${1}"

if [ -z "${project}" ] ; then
    printf "Connectome DB Project: "
    read project
fi

subject="${2}"

if [ -z "${subject}" ] ; then
    printf "Subject: "
    read subject
fi

mkdir -p ${project}

python ../CheckHcpPipelineStatus.py \
    --verbose=true \
    -u ${userid} \
    -p ${password} \
    -pl structural \
    -pr "${project}" \
    -o "${project}/${subject}.out" \
    -su "${subject}"

more ${project}/${subject}.out
