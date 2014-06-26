#!/bin/bash

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subj="${1}"

python ../CheckHcpPipelineStatus.py \
    --verbose=True \
    -u tbbrown \
    -p ${password} \
    -pl functional \
    -pr HCP_Staging \
    -o "${subj}.out" \
    -su "${subj}"

more "${subj}.out"