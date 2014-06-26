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
    -o "Batch11.out" \
    -su "979984,983773,984472,987983,991267,992774,994273"



