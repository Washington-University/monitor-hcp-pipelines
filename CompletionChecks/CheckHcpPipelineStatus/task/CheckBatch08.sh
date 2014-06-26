#!/bin/bash

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

completeSubjList="441939,445543,448347,465852,473952,475855,479762,480141,485757,486759,497865,499566,500222,510326,519950,521331,522434,530635,531536,540436,541640,541943,545345,547046,552544,559053,561242,562446,565452,566454,567052,567961,568963,570243,573249,573451,579665,580044,580347,581349,583858,585862,586460,592455,594156,598568,599065"

subjList="559053"

rm Batch08.out
touch Batch08.out

for subj in ${subjList} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl task \
        -pr HCP_Staging \
        -o "${subj}.out" \
        -su "${subj}"

    grep -v "SubjectID" ${subj}.out >> Batch08.out

done
