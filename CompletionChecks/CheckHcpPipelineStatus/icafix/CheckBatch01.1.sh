#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subjList="100307,100408,101006,101107,101309,101410,101915,102008,102311,102816"

python ../CheckHcpPipelineStatus.py \
    --verbose=True \
    -u ${username} \
    -p ${password} \
    -pl fixl \
    -pr HCP_Staging \
    -o "Batch01.1.out" \
    -su "${subjList}"

