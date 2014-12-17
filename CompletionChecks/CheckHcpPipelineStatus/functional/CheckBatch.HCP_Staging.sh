#!/bin/bash

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

subject_files_dir=~/subject_list_files
project="HCP_Staging"
subject_file_name="${subject_files_dir}/${project}.functional.subjects"
echo "Retrieving subject list from: ${subject_file_name}"
subject_list_from_file=( $( cat ${subject_file_name} ) )
subjects="`echo "${subject_list_from_file[@]}"`"

mkdir -p ${project}

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
        -pr ${project} \
        -o "${project}/${subject}.out" \
        -su "${subject}"

    more "${project}/${subject}.out"
done
