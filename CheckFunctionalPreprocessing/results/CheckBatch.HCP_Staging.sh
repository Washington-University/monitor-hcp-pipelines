#!/bin/bash

subject_files_dir=~/subject_list_files
project="HCP_Staging"
subject_file_name="${subject_files_dir}/${project}.functional.subjects"
echo "Retrieving subject list from: ${subject_file_name}"
subject_list_from_file=( $( cat ${subject_file_name} ) )
subjects="`echo "${subject_list_from_file[@]}"`"

mkdir -p ${project}

for subject in $subjects ; do
    echo "Checking subject: ${subject}"
    ../CheckFunctionalPreprocessing.sh --project=${project} --subjects=${subject} | tee ${project}/${subject}.out | grep FAIL
done
