#!/bin/bash

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

project="HCP_Staging_RT"

from_file=( $( cat ${project}.functional.subjects ) )
subjects="`echo "${from_file[@]}"`"

for subject in $subjects ; do
    echo "Checking functional preprocessing completeness for subject: ${subject} in project: ${project}"

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${userid} \
        -p ${password} \
        -pl functional \
        -pr "${project}" \
        -o "${subject}.out" \
        -su "${subject}"

    more "${subject}.out"
done
