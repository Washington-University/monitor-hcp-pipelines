#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subjList="979984,983773,984472,987983,991267,992774,994273"

python ../CheckHcpPipelineStatus.py \
    --verbose=True \
    -u ${username} \
    -p ${password} \
    -pl fixl \
    -pr HCP_Staging \
    -o "Batch11.out" \
    -su "${subjList}"

