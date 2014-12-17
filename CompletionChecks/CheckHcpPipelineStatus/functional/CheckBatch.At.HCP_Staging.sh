#!/bin/bash

#printf "Connectome DB Username: "
#read userid
userid="tbbrown"

#stty -echo
#printf "Connectome DB Password: "
#read password
#echo ""
#stty echo
password="ThisIsNotMyPassword"

project="HCP_Staging"
subjects="970764"

for subject in $subjects ; do
    echo "Checking functional preprocessing completeness for subject: ${subject} in project: ${project}"

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${userid} \
        -p ${password} \
        -pl functional \
        -pr ${project} \
        -o "${subject}.out" \
        -su "${subject}"

    more "${subject}.out"
done
