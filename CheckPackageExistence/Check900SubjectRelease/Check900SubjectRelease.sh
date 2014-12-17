#!/bin/bash

subject_files_dir=~/subject_list_files
subject_file_name="${subject_files_dir}/Full900SubjectsRelease.subjects"
echo "Retrieving subject list from: ${subject_file_name}"
subject_list_from_file=( $( cat ${subject_file_name} ) )
subjects="`echo "${subject_list_from_file[@]}"`"

for subject in ${subjects} ; do
    ../CheckPackageExistence.sh --subject=${subject} | tee ${subject}.out
done

