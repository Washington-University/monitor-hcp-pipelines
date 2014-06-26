#!/bin/bash

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

python ../CheckHcpPipelineStatus.py \
    --verbose=true \
    -u tbbrown \
    -p ${password} \
    -pl structural \
    -pr HCP_Staging \
    -o "366446.out" \
    -su "366446"
