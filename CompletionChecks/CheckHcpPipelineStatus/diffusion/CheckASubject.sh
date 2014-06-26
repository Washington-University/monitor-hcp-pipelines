#!/bin/bash

printf "Connectome DB Username: "
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

printf "Subject ID: " 
read subj

python ../CheckHcpPipelineStatus.py \
    --verbose=True \
    -u "${username}" \
    -p "${password}" \
    -pl diffusion \
    -pr HCP_Staging \
    -o "${subj}.out" \
    -su "${subj}"

more "${subj}.out"
