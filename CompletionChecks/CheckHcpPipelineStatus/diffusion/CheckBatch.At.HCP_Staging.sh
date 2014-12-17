#!/bin/bash

#printf "Connectome DB Username: "
#read username
username="tbbrown"

#stty -echo
#printf "Connectome DB Password: "
#read password
#echo ""
#stty echo
password="ThisIsNotMyPassword"

project="HCP_Staging"
subjects="970764 136631"

for subject in ${subjects} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u "${username}" \
        -p "${password}" \
        -pl diffusion \
        -pr "${project}" \
        -o "${subject}.out" \
        -su "${subject}"
    
    more "${subject}.out"

done