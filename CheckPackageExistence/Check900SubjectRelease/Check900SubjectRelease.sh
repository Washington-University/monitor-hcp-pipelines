#!/bin/bash

subject_files_dir=~/subject_list_files
subject_file_name="${subject_files_dir}/Full900SubjectsRelease.subjects"
echo "Retrieving subject list from: ${subject_file_name}"
subject_list_from_file=( $( cat ${subject_file_name} ) )
subjects="`echo "${subject_list_from_file[@]}"`"

rm -f Full900SubjectsRelease.out
for subject in ${subjects} ; do
	../CheckPackageExistence.sh --subject=${subject} --rootdir=/data/hcpdb/packages/prerelease/zip/HCP_900 | tee ${subject}.out
	cat ${subject}.out >> Full900SubjectsRelease.out
done

