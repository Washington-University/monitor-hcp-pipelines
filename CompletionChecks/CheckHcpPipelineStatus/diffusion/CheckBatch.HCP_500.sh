#!/bin/bash

printf "Connectome DB Username: "
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

project="HCP_500"

from_file=( $( cat ${project}.diffusion.subjects ) )
subjects="`echo "${from_file[@]}"`"

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