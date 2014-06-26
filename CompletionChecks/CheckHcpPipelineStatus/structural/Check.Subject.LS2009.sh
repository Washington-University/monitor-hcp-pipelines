#!/bin/bash

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subject="LS2009"

python ../CheckHcpPipelineStatus.py \
    --verbose=true \
    -u tbbrown \
    -p ${password} \
    -pl structural \
    -pr PipelineTest \
    -o "${subject}.out" \
    -su "${subject}"
