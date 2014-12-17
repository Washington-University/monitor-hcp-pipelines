#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

project="WU_L1A_Staging"
from_file=( $( cat ${project}.icafix.subjects ) )
subjects="`echo "${from_file[@]}"`"

for subject in ${subjects} ; do

    echo "Checking Subject: ${subject}"

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl fix \
        -itn "rfMRI_REST1,rfMRI_REST2,rfMRI_REST3,rfMRI_REST4,rfMRI_REST5" \
        -pr ${project} \
        -o "${subject}.out" \
        -su "${subject}"

    more "${subject}.out"

done
