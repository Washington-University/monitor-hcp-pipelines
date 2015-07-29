#!/bin/bash

ARCHIVE_ROOT="/data/hcpdb/archive"
ARCHIVE_PROJ_SUBDIR="arc001"
TESLA_SPEC="_3T"

usage() {
	echo "Usage information TBW"
}

get_options() {
    local arguments=($@)

    # initialize global output variables
    unset g_project
	unset g_subject
	unset g_details
	g_details="FALSE"

    # parse arguments
    local index=0
    local numArgs=${#arguments[@]}
    local argument

    while [ ${index} -lt ${numArgs} ]; do
        argument=${arguments[index]}

        case ${argument} in
            --help)
                usage
                exit 1
                ;;
            --project=*)
                g_project=${argument/*=/""}
                index=$(( index + 1 ))
                ;;
            --subject=*)
                g_subject=${argument/*=/""}
                index=$(( index + 1 ))
				;;
			--details)
				g_details="TRUE"
				index=$(( index + 1 ))
                ;;
            *)
                echo "Unrecognized Option: ${argument}"
                usage
                exit 1
                ;;
        esac
    done

    # check required parameters
	local error_count=0

    if [ -z ${g_project} ]; then
        echo "ERROR: --project=<project-name> is required."
        error_count=$(( error_count + 1 ))
    fi

    if [ -z ${g_subject} ]; then
        echo "ERROR: --subject=<subject-id> is required."
        error_count=$(( error_count + 1 ))
    fi

	if [ "${error_count}" -gt 0 ]; then
		usage
		exit 1
	fi
}

main() {

	host=`hostname`
	if [ "${host}" != "hcpx-fs01.nrg.mir" ] ; then
		echo "ERROR: This script is intended to be run on host: hcpx-fs01.nrg.mir"
		exit 1
	fi

	get_options $@

	echo ""
	echo "Project: ${g_project}"
	echo "Subject: ${g_subject}"

	presentDir=`pwd`
	archiveDir="${ARCHIVE_ROOT}/${g_project}/${ARCHIVE_PROJ_SUBDIR}/${g_subject}${TESLA_SPEC}"
	#echo "archiveDir: ${archiveDir}"

	scans="rfMRI_REST1_LR"
	scans+=" rfMRI_REST1_RL"
	scans+=" rfMRI_REST2_LR"
	scans+=" rfMRI_REST2_RL"

	#echo "scans: ${scans}"

	file_suffixes="_Atlas_BiasField.dscalar.nii"
	file_suffixes+=" _Atlas_CleanedMGT.txt"
	file_suffixes+=" _Atlas_HighPassMGT.txt"
	file_suffixes+=" _Atlas_hp2000_clean_vn.dscalar.nii"
	file_suffixes+=" _Atlas_NoiseMGT.txt"
	file_suffixes+=" _Atlas_OrigMGT.txt"
	file_suffixes+=" _Atlas_PostMotionMGT.txt"
	file_suffixes+=" _Atlas_stats.dscalar.nii"
	file_suffixes+=" _Atlas_stats.txt"
	file_suffixes+=" _Atlas_UnstructNoiseMGT.txt"

	for scan in ${scans} ; do
		# does Resting State States Resource exist

		resourceDir=${archiveDir}/RESOURCES/${scan}_PostFix
		if [ -d "${resourceDir}" ] ; then
			resource_exists="TRUE"
		else
			resource_exists="FALSE"
		fi
		
		all_files_exist="TRUE"
		for suffix in ${file_suffixes} ; do
			filename="${resourceDir}/${g_subject}/MNINonLinear/Results/${scan}/${scan}${suffix}"
			
			if [ ! -e "${filename}" ] ; then
				all_files_exist="FALSE"

				if [ "${g_details}" = "TRUE" ]; then
					echo "Does not exist: ${filename}"
				fi
			fi
		done

		echo -e "\tScan: ${scan}\tResource Exists: ${resource_exists}\tFiles Exist: ${all_files_exist}"
	done
}

main $@
