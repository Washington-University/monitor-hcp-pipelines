#!/bin/bash

printf "Connectome DB Username: "
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

python ../CheckHcpPipelineStatus.py \
    --verbose=True \
    -u ${username} \
    -p ${password} \
    -pl functional \
    -pr HCP_Staging \
    -o "Batch14.out" \
    -su "108323,151728,161327,161630,166438,172938,199554,208428,211215,231928,251833,339847,361941,382242,390645,571548,599469,749361,779370,792766,816653,957974,959069"
