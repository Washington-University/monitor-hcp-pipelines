#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

# subjects=""
# subjects="${subjects} LS2001 LS2003 LS2008 LS2009 LS2037 LS2043 LS3017 LS3019 LS3026 LS3029 "
# subjects="${subjects} LS3040 LS3046 LS4025 LS4036 LS4041 LS4043 LS4047 LS5041 "

# subjects="LS2009 LS4041"

subjects="LS5007"

project="WU_L1A_Staging"

for subject in ${subjects} ; do

    echo "Checking Subject: ${subject}"

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl fix \
        -itn "rfMRI_REST1,rfMRI_REST2,rfMRI_REST3,rfMRI_REST4,rfMRI_REST5" \
        -pr ${project} \
        -o "${subject}.out" \
        -su "${subject}"

    more "${subject}.out"

done
