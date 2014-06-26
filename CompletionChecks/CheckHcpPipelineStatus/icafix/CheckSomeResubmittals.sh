#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subjList="251833,871964,304020,169141"

python ../CheckHcpPipelineStatus.py \
    --verbose=True \
    -u ${username} \
    -p ${password} \
    -pl fixl \
    -pr HCP_Staging \
    -o "SomeResubmittals.out" \
    -su "${subjList}"

