#!/bin/bash

check_subject()
{
    echo ""
    echo "--------------------------------------------------------------------------------"
    echo " Checking Functional Preprocessing completeness for subject: ${subject} in project: ${project}"
    echo "--------------------------------------------------------------------------------"
    echo ""

    python ../CheckHcp7TPipelineStatus.py \
        --verbose=True \
        -u ${userid} \
        -p ${password} \
        -pl functional \
        -pr "${project}" \
        -o "${project}/${subject}.out" \
        -su "${subject}"

    cat "${project}/${subject}.out"
}


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

project="HCP_Staging_7T"
subject_file_name="${SUBJECT_FILES_DIR}/${project}.functional.subjects"
echo "Retrieving subject list from: ${subject_file_name}"
subject_list_from_file=( $( cat ${subject_file_name} ) )
subjects="`echo "${subject_list_from_file[@]}"`"

mkdir -p ${project}

for subject in ${subjects}
do
	case ${subject} in
		StopProcessing*)
			exit;
			;;
		*)
			check_subject
			;;
	esac
done
