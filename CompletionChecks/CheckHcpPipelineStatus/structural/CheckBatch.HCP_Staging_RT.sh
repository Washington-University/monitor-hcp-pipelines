#!/bin/bash

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subjects=""
subjects="${subjects} 187547 287248 341834 660951 "

project="HCP_Staging_RT"

for subject in ${subjects} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=true \
        -u ${userid} \
        -p ${password} \
        -pl structural \
        -pr ${project} \
        -o "${subject}.out" \
        -su "${subject}"

    cat ${subject}.out >> CheckABatch.HCP_Staging_RT.out

done