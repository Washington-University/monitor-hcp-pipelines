#!/bin/bash

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

# subjects=""
# subjects="${subjects} LS2003 LS2008 LS2037 LS2043 LS3019 LS3026 LS3029 LS3040 LS3046 LS4004 "
# subjects="${subjects} LS4025 LS4036 LS4041 LS4043 LS4047 LS5041 "

subjects="LS4004 LS5007"

project="WU_L1A_Staging"

for subject in ${subjects} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=true \
        -u ${userid} \
        -p ${password} \
        -pl structural \
        -pr ${project} \
        -o "${subject}.out" \
        -su "${subject}"

    # cat ${subject}.out >> CheckBatch.${project}.out
    cat ${subject}.out

done