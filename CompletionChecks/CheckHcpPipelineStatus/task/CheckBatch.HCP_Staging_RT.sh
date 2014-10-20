#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

# subjects=""
# subjects="${subjects} 103818 122317 137128 139839 143325 149337 151526 158035 175439 177746 "
# subjects="${subjects} 185442 192439 194140 195041 250427 599671 662551 783462 859671 861456 "
# subjects="${subjects} 917255 "

subjects="341834"


project=HCP_Staging_RT

for subject in ${subjects} ; do

    echo "Checking Subject: ${subject}"

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl task \
        -pr ${project} \
        -o "${subject}.out" \
        -su "${subject}"

    more "${subject}.out"

done