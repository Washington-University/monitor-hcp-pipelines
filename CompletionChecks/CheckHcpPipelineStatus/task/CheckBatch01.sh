#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

# complete list of batch 01 subjects
completeSubjList="100307,100408,101006,101107,101309,101410,101915,102008,102311,102816,103111,103414,103515,103818,104820,105014,105115,105216,106016,106319,106521,107321,107422,108121,108525,108828,109123,109325,110411,111312,111413,111716,112819,113215,113619,113821,113922,114419,114924,115320,116120,116524,117122,117324,118528,118730,118932,119833,120111,120212"

# list of those that need checking
subjList="101107"

rm Batch01.out
touch Batch01.out

for subj in ${subjList} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl task \
        -pr HCP_Staging \
        -o "${subj}.out" \
        -su "${subj}"

    grep -v "SubjectID" ${subj}.out >> Batch01.out

done
