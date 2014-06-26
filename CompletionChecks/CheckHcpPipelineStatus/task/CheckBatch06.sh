#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

completeSubjList="199655,199958,200109,200614,201111,201414,201818,203418,204016,204521,205119,205220,205725,205826,208024,208226,208327,209834,209935,210011,210415,210617,211316,211417,211720,211922,212116,212217,212318,212419,214019,214221,214423,214726,217126,217429,219231,221319,224022,233326,239944,245333,246133,249947,250427"

subjList="210415 250427"

rm Batch06.out
touch Batch06.out

for subj in ${subjList} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl task \
        -pr HCP_Staging \
        -o "${subj}.out" \
        -su "${subj}"

    grep -v "SubjectID" ${subj}.out >> Batch06.out

done
