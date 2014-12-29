#!/bin/bash

#printf "Connectome DB Username: " 
#read username
username="tbbrown"

# stty -echo
# printf "Connectome DB Password: "
# read password
# echo ""
# stty echo
password="ThisIsNotMyPassword"

project="HCP_Staging"

subjects=""
subjects="${subjects} 136631"
subjects="${subjects} 146634"
subjects="${subjects} 154330"
subjects="${subjects} 170631"
subjects="${subjects} 173233"
subjects="${subjects} 174437"
subjects="${subjects} 176239"
subjects="${subjects} 182436"
subjects="${subjects} 185947"
subjects="${subjects} 190132"
subjects="${subjects} 193441"
subjects="${subjects} 194746"
subjects="${subjects} 204218"
subjects="${subjects} 204319"
subjects="${subjects} 208125"
subjects="${subjects} 209127"
subjects="${subjects} 219231"
subjects="${subjects} 220721"
subjects="${subjects} 227432"
subjects="${subjects} 228434"
subjects="${subjects} 239136"
subjects="${subjects} 270332"
subjects="${subjects} 295146"
subjects="${subjects} 300618"
subjects="${subjects} 322224"
subjects="${subjects} 336841"
subjects="${subjects} 378857"
subjects="${subjects} 381038"
subjects="${subjects} 384448"
subjects="${subjects} 389357"
subjects="${subjects} 393247"
subjects="${subjects} 393550"
subjects="${subjects} 429040"
subjects="${subjects} 453441"
subjects="${subjects} 467351"
subjects="${subjects} 468050"
subjects="${subjects} 513736"
subjects="${subjects} 529549"
subjects="${subjects} 536647"
subjects="${subjects} 541640"
subjects="${subjects} 548250"
subjects="${subjects} 572045"
subjects="${subjects} 587664"
subjects="${subjects} 590047"
subjects="${subjects} 609143"
subjects="${subjects} 615744"
subjects="${subjects} 645450"
subjects="${subjects} 654350"
subjects="${subjects} 656253"
subjects="${subjects} 680250"
subjects="${subjects} 688569"
subjects="${subjects} 707749"
subjects="${subjects} 720337"
subjects="${subjects} 727553"
subjects="${subjects} 734247"
subjects="${subjects} 737960"
subjects="${subjects} 763557"
subjects="${subjects} 810439"
subjects="${subjects} 815247"
subjects="${subjects} 818455"
subjects="${subjects} 818859"
subjects="${subjects} 844961"
subjects="${subjects} 867468"
subjects="${subjects} 872562"
subjects="${subjects} 873968"
subjects="${subjects} 880157"
subjects="${subjects} 882161"
subjects="${subjects} 884064"
subjects="${subjects} 894067"
subjects="${subjects} 902242"
subjects="${subjects} 942658"
subjects="${subjects} 947668"
subjects="${subjects} 955465"
subjects="${subjects} 996782"

mkdir -p ${project}

for subject in ${subjects} ; do

    echo "Checking ICA FIX Completion for Subject: ${subject} in Project: ${project}"

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl fix \
        -pr ${project} \
        -o "${project}/${subject}.out" \
        -su "${subject}"

    more "${project}/${subject}.out"

done
