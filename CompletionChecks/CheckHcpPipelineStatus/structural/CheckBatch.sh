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

project="${1}"

if [ -z "${project}" ] ; then
    printf "Connectome DB Project: "
    read project
fi

subject_file_name="${SUBJECT_FILES_DIR}/${project}.structural.subjects"
echo "Retrieving subject list from: ${subject_file_name}"
subject_list_from_file=( $( cat ${subject_file_name} ) )
subjects="`echo "${subject_list_from_file[@]}"`"

mkdir -p ${project}

for subject in ${subjects} ; do

    python ../CheckHcpPipelineStatus.py \
        --verbose=true \
        -u ${userid} \
        -p ${password} \
        -pl structural \
        -pr ${project} \
        -o "${project}/${subject}.out" \
        -su "${subject}"

    more ${project}/${subject}.out 

done
