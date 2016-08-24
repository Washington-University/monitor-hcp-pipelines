#!/bin/bash

printf "Project: (e.g. HCP_900, HCP_500, HCP_Staging): "
read project

printf "Subject List File: "
read subject_file_name

echo "Retrieving subject list from: ${subject_file_name}"
subject_list_from_file=( $( cat ${subject_file_name} ) )
subjects="`echo "${subject_list_from_file[@]}"`"

output_file_name="CheckSpecified.${project}.out"
rm -f ${output_file_name}

for subject in ${subjects} ; do
	../CheckPackageExistence.sh \
		--subject=${subject} \
		--suppress-checksum-regen \
		--rootdir=/data/hcpdb/packages/prerelease/zip/${project} | tee ${project}.${subject}.out
	cat ${project}.${subject}.out >> ${output_file_name}
done

