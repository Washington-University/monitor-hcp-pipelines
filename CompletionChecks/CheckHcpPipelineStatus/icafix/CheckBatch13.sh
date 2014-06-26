#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subjList="142424,169141"

python ../CheckHcpPipelineStatus.py \
    --verbose=True \
    -u ${username} \
    -p ${password} \
    -pl fixl \
    -pr HCP_Staging \
    -o "Batch13.out" \
    -su "${subjList}"

