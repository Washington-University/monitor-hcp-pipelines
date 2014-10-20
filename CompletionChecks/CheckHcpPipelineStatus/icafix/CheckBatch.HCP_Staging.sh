#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subjects=""
subjects="${subjects} 105923 114823 130518 139839 146129 287248 562345 662551 783462 "

project="HCP_Staging"

for subject in ${subjects} ; do

    echo "Checking Subject: ${subject}"

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl fix \
        -pr ${project} \
        -o "${subject}.out" \
        -su "${subject}"

    more "${subject}.out"

done
