#!/bin/bash

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subject="${1}"

if [ -z "${subject}" ] ; then
    printf "Subject: "
    read subject
fi

python ../CheckHcpPipelineStatus.py \
    --verbose=true \
    -u ${userid} \
    -p ${password} \
    -pl structural \
    -pr WU_L1A_Staging \
    -o "${subject}.out" \
    -su "${subject}"
