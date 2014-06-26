#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

#subjList="158035,158136,158540,159138,159239,159340,159441,160123,160830,161731,162026,162228,162329,162733,163129,163331,163432,163836,164030,164131,164939,165032,165840,167036,167743,168139,168341,169343,169444,170934,171431,171633,172029,172130,172332,172534,173132,173334,173435,173536,173940,175035,175439,176542,177645"

subjList="167036,168139,172029,172534,173132,175035"

python ../CheckHcpPipelineStatus.py \
    --verbose=True \
    -u ${username} \
    -p ${password} \
    -pl diffusion \
    -pr HCP_Staging \
    -o "Batch04.out" \
    -su "${subjList}"



