#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

# complete list of batch 11 subjects
completeSubjList="979984,983773,984472,987983,991267,992774,994273"

# list of those that need checking
subjList="979984 983773 984472 987983 991267 992774 994273"

rm Batch11.out
touch Batch11.out

for subj in ${subjList} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl task \
        -pr HCP_Staging \
        -o "${subj}.out" \
        -su "${subj}"

    grep -v "SubjectID" ${subj}.out >> Batch11.out

done
