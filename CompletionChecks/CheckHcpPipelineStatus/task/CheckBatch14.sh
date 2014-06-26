#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

# complete list of batch 14 subjects
completeSubjList="108323,151728,161327,161630,166438,172938,191336,194847,199554,208428,211215,231928,339847,361941,382242,571548,599469,749361,779370,792766,816653,957974,959069"

# list of those that need checking
subjList="108323 151728 161327 161630 166438 172938 191336 194847 199554 208428 211215 231928 339847 361941 382242 571548 599469 749361 779370 792766 816653 957974 959069"

rm Batch14.out
touch Batch14.out

for subj in ${subjList} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl task \
        -pr HCP_Staging \
        -o "${subj}.out" \
        -su "${subj}"

    grep -v "SubjectID" ${subj}.out >> Batch14.out

done

