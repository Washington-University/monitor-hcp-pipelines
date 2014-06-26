#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

completeSubjList="178142,178748,178849,178950,179346,179548,180129,180432,180836,180937,181131,181232,182739,182840,183034,185139,186141,187143,187547,187850,188347,189349,189450,190031,191033,191437,191841,192439,192540,192843,193239,194140,194645,195041,195647,195849,196144,196750,197348,197550,197651,198350,198451,198855,199150,199251,199453"

subjList="183034"

rm Batch05.out
touch Batch05.out

for subj in ${subjList} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl task \
        -pr HCP_Staging \
        -o "${subj}.out" \
        -su "${subj}"

    grep -v "SubjectID" ${subj}.out >> Batch05.out

done
