#!/bin/bash

printf "Connectome DB Username: "
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

project="WU_L1A_Staging"

from_file=( $( cat ${project}.diffusion.subjects ) )
subjects="`echo "${from_file[@]}"`"

for subject in ${subjects} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u "${username}" \
        -p "${password}" \
        -pl diffusion \
        --diffusion-voxel-size="1.50" \
        -pr "${project}" \
        -o "${subject}.out" \
        -su "${subject}"
    
    more "${subject}.out"

done