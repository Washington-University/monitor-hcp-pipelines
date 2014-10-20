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
    printf "Project: "
    read project
fi

subject="${2}"

if [ -z "${subject}" ] ; then
    printf "Subject: "
    read subject
fi

python ../CheckHcpPipelineStatus.py \
    --verbose=true \
    -u ${userid} \
    -p ${password} \
    -pl structural \
    -pr "${project}" \
    -o "${subject}.out" \
    -su "${subject}"
