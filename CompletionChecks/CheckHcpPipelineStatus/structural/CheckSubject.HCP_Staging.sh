#!/bin/bash

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

printf "Subject(s) (comma separated): "
read subject

python ../CheckHcpPipelineStatus.py \
    --verbose=true \
    -u ${userid} \
    -p ${password} \
    -pl structural \
    -pr HCP_Staging \
    -o "${subject}.out" \
    -su "${subject}"
