#!/bin/bash

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

python ../CheckHcpPipelineStatus.py \
    -u tbbrown \
    -p ${password} \
    -pl structural \
    -pr HCP_Staging \
    -o "Batch13.out" \
    -su "142424,165234,169141"
