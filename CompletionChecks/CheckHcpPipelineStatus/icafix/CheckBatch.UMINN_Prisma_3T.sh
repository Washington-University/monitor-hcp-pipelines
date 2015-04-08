#!/bin/bash

if [ -z "${SUBJECT_FILES_DIR}" ] ; then
    echo "Environment variable SUBJECT_FILES_DIR must be set!"
    exit 1
fi

printf "Connectome DB Username: " 
read username

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

project="WU_L37_Staging"
subject_file_name="${SUBJECT_FILES_DIR}/${project}.icafix.subjects"
echo "Retrieving subject list from: ${subject_file_name}"
subject_list_from_file=( $( cat ${subject_file_name} ) )
subjects="`echo "${subject_list_from_file[@]}"`"

mkdir -p ${project}

for subject in ${subjects} ; do
    echo ""
    echo "--------------------------------------------------------------------------------"
    echo " Checking ICA FIX Processing completeness for subject: ${subject} in project: ${project}"
    echo "--------------------------------------------------------------------------------"
    echo ""

    python ../CheckHcpPipelineStatusPrisma3T.py \
        --verbose=True \
        -u ${username} \
        -p ${password} \
        -pl fix \
        -itn "rfMRI_REST1,rfMRI_REST2,rfMRI_REST3,rfMRI_REST4,rfMRI_REST5,rfMRI_REST6,rfMRI_REST7,rfMRI_REST8,rfMRI_REST9" \
        -pr ${project} \
        -o "${project}/${subject}.out" \
        -su "${subject}"

    more "${project}/${subject}.out"

done
