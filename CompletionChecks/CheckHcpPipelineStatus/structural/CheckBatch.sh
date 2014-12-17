#!/bin/bash

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

subject_files_dir=~/subject_list_files
subject_file_name="${subject_files_dir}/${project}.structural.subjects"
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