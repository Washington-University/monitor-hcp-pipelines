#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subj="177746"

python ../CheckHcpPipelineStatus.py \
    --verbose=True \
    -u ${username} \
    -p ${password} \
    -pl task \
    -pr HCP_500 \
    -o "${subj}.out" \
    -su "${subj}"

more "${subj}.out"