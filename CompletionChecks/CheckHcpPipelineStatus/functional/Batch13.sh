#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

python ../CheckHcpPipelineStatus.py \
    --verbose=True \
    -u ${username} \
    -p ${password} \
    -pl functional \
    -pr HCP_Staging \
    -o "Batch13.out" \
    -su "142424,169141"



