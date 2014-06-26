#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

# complete list of batch 02 subjects
completeSubjList="120515,121315,121618,122317,122620,123117,123420,123925,124220,124422,124826,125525,126325,126628,127630,127933,128127,128329,128632,129028,129533,130013,130316,130922,131217,131722,131924,132118,133019,133625,133827,133928,134324,135225,135528,135932,136227,136833,137027,137128,137633,137936,138231,138534,139233,139637,140117"

# list of those that need checking
subjList=""

rm Batch02.out
touch Batch02.out

for subj in ${subjList} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl task \
        -pr HCP_Staging \
        -o "${subj}.out" \
        -su "${subj}"

    grep -v "SubjectID" ${subj}.out >> Batch02.out

done
