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

project="HCP_Staging"
subject_file_name="${SUBJECT_FILES_DIR}/${project}.diffusion.subjects"
echo "Retrieving subject list from: ${subject_file_name}"
subject_list_from_file=( $( cat ${subject_file_name} ) )
subjects="`echo "${subject_list_from_file[@]}"`"

mkdir -p ${project}

for subject in ${subjects} ; do

	if [[ ! ${subject} == \#* ]] ; then
		echo ""
		echo "--------------------------------------------------------------------------------"
		echo " Checking Diffusion Preprocessing completeness for subject: ${subject} in project: ${project}"
		echo "--------------------------------------------------------------------------------"
		echo ""
		
		python ../CheckHcpPipelineStatus.py \
			--verbose=True \
			-u "${username}" \
			-p "${password}" \
			-pl diffusion \
			-pr "${project}" \
			-o "${project}/${subject}.out" \
			-su "${subject}"
		
		more "${project}/${subject}.out"
		
	fi
done
