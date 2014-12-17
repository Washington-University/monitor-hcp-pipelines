#!/bin/bash

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subject_files_dir=~/subject_list_files
project="WU_L1A_Staging"
subject_file_name="${subject_files_dir}/${project}.functional.subjects"
echo "Retrieving subject list from: ${subject_file_name}"
subject_list_from_file=( $( cat ${subject_file_name} ) )
subjects="`echo "${subject_list_from_file[@]}"`"

for subject in $subjects ; do
    echo ""
    echo "--------------------------------------------------------------------------------"
    echo " Checking Functional Preprocessing completeness for subject: ${subject} in project: ${project}"
    echo "--------------------------------------------------------------------------------"
    echo ""

    python ../CheckHcpPipelineStatus.py \
        --verbose=True \
        -u ${userid} \
        -p ${password} \
        -pl functional \
        -ftn "rfMRI_REST1,rfMRI_REST2,rfMRI_REST3,rfMRI_REST4,tfMRI_WM,tfMRI_GAMBLING,tfMRI_SOCIAL,tfMRI_EMOTION" \
        -pr "${project}" \
        -o "${subject}.out" \
        -su "${subject}"

    more "${subject}.out"
done
