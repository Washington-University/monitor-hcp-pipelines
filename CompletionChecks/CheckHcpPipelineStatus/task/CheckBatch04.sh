#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

# complete list of batch 04 subjects
completeSubjList="158035,158136,158540,159138,159239,159340,159441,160123,160830,161731,162026,162228,162329,162733,163129,163331,163432,163836,164030,164131,164939,165032,165840,167036,167743,168139,168341,169343,169444,170934,171431,171633,172029,172130,172332,172534,173132,173334,173435,173536,173940,175035,175439,176542,177645"

# list of those that need checking
subjList=""

rm Batch04.out
touch Batch04.out

for subj in ${subjList} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl task \
        -pr HCP_Staging \
        -o "${subj}.out" \
        -su "${subj}"

    grep -v "SubjectID" ${subj}.out >> Batch04.out

done
    
