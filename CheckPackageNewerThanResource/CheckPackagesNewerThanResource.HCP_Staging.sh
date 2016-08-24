#!/bin/bash

project="HCP_Staging"

subject_files_dir=~/subject_list_files
subject_file_name="${subject_files_dir}/${project}.subjects"
echo "Retrieving subject list from: ${subject_file_name}"
subject_list_from_file=( $( cat ${subject_file_name} ) )
subjects="`echo "${subject_list_from_file[@]}"`"

for subject in ${subjects} ; do
	if [[ ${subject} != \#* ]]; then
		./CheckPackagesNewerThanResource.OneSubject.sh --subject=${subject} --project=${project}
	fi
done
