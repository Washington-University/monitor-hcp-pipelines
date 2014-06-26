#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

completeSubjList="788876,789373,792564,802844,814649,826353,826454,833148,833249,837560,837964,845458,849971,856766,857263,859671,861456,865363,871762,872158,872764,877168,877269,885975,887373,889579,894673,896778,896879,898176,899885,901038,901139,901442,904044,907656,910241,912447,917255,922854,930449,932554,951457,958976,959574,965367,965771,978578,937160"

subjList="792564"

rm Batch10.out
touch Batch10.out

for subj in ${subjList} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl task \
        -pr HCP_Staging \
        -o "${subj}.out" \
        -su "${subj}"

    grep -v "SubjectID" ${subj}.out >> Batch10.out

done
