#!/bin/bash

subjectList="779370 792766 816653 957974 959069"


stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

for subj in ${subjectList} ; do
    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u tbbrown \
        -p ${password} \
        -pl functional \
        -pr HCP_Staging \
        -o "${subj}.out" \
        -su "${subj}"
done


