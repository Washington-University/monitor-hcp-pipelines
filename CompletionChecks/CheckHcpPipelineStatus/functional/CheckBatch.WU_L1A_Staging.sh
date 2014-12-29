#!/bin/bash

if [ -z "${SUBJECT_FILES_DIR}" ] ; then
    echo "Environment variable SUBJECT_FILES_DIR must be set!"
    exit 1
fi

printf "Connectome DB Username: "
read userid

stty -echo
printf "Connectome DB Password: "
read password
echo ""
stty echo

project="WU_L1A_Staging"
subject_file_name="${SUBJECT_FILES_DIR}/${project}.functional.subjects"
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
        -ftn "rfMRI_REST1,rfMRI_REST2,rfMRI_REST3,rfMRI_REST4,tfMRI_WM,tfMRI_GAMBLING,tfMRI_SOCIAL,tfMRI_EMOTION" \
        -pr "${project}" \
        -o "${project}/${subject}.out" \
        -su "${subject}"

    more "${project}/${subject}.out"
done
