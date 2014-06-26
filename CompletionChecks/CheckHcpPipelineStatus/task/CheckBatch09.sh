#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

completeSubjList="599671,601127,613538,620434,622236,623844,627549,638049,644044,645551,650746,654754,665254,672756,673455,677968,679568,680957,683256,685058,687163,690152,695768,702133,704238,705341,709551,713239,715041,715647,729254,729557,732243,734045,742549,748258,748662,751348,753251,756055,759869,761957,765056,770352,771354,782561,784565,786569"

subjList="673455 742549"

rm Batch09.out
touch Batch09.out

for subj in ${subjList} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl task \
        -pr HCP_Staging \
        -o "${subj}.out" \
        -su "${subj}"

    grep -v "SubjectID" ${subj}.out >> Batch09.out

done

