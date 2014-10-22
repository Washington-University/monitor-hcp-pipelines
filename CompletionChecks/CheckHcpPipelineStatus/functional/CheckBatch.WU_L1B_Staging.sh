#!/bin/bash

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

project="WU_L1B_Staging"

from_file=( $( cat ${project}.functional.subjects ) )
subjects="`echo "${from_file[@]}"`"

for subject in $subjects ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${userid} \
        -p ${password} \
        -pl functional \
        -ftn "rfMRI_REST1,rfMRI_REST2,rfMRI_REST3,rfMRI_REST4,rfMRI_REST5,rfMRI_REST6,tfMRI_WM,tfMRI_GAMBLING,tfMRI_SOCIAL,tfMRI_EMOTION" \
        -pr "${project}" \
        -o "${subject}.out" \
        -su "${subject}"

    more "${subject}.out"
done
