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

	# does MSMAllDeDrift resource exist
	msm_all_dedrift_resource_dir=${archiveDir}/RESOURCES/MSMAllDeDrift

	if [ -d "${msm_all_dedrift_resource_dir}" ] ; then
		resource_exists="TRUE"
	else
		resource_exists="FALSE"
	fi

	#echo "msm_all_dedrift_resource_dir: ${msm_all_dedrift_resource_dir}"
	#echo "resource_exists: ${resource_exists}"

	files=""

	check_dir="${msm_all_dedrift_resource_dir}/MNINonLinear"
	files+=" ${check_dir}/${g_subject}.ArealDistortion_MSMAll.164k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.corrThickness_MSMAll.164k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.curvature_MSMAll.164k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.EdgeDistortion_MSMAll.164k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.L.inflated_MSMAll.164k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.L.midthickness_MSMAll.164k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.L.pial_MSMAll.164k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.L.very_inflated_MSMAll.164k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.L.white_MSMAll.164k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.MSMAll.164k_fs_LR.wb.spec"
	files+=" ${check_dir}/${g_subject}.MyelinMap_BC_MSMAll.164k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.R.inflated_MSMAll.164k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.R.midthickness_MSMAll.164k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.R.pial_MSMAll.164k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.R.very_inflated_MSMAll.164k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.R.white_MSMAll.164k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.SmoothedMyelinMap_BC_MSMAll.164k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.SphericalDistortion_MSMAll.164k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.sulc_MSMAll.164k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.thickness_MSMAll.164k_fs_LR.dscalar.nii"

	check_dir="${msm_all_dedrift_resource_dir}/MNINonLinear/fsaverage_LR32k"
	files+=" ${check_dir}/${g_subject}.ArealDistortion_MSMAll.32k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.BiasField_MSMAll.32k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.corrThickness_MSMAll.32k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.curvature_MSMAll.32k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.EdgeDistortion_MSMAll.32k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.L.inflated_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.L.midthickness_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.L.pial_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.L.very_inflated_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.L.white_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.MSMAll.32k_fs_LR.wb.spec"
	files+=" ${check_dir}/${g_subject}.MyelinMap_BC_MSMAll.32k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.MyelinMap_MSMAll.32k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.R.inflated_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.R.midthickness_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.R.pial_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.R.very_inflated_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.R.white_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.SmoothedMyelinMap_BC_MSMAll.32k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.SphericalDistortion_MSMAll.32k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.sulc_MSMAll.32k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.thickness_MSMAll.32k_fs_LR.dscalar.nii"
	
	check_dir="${msm_all_dedrift_resource_dir}/MNINonLinear/Native"
	files+=" ${check_dir}/${g_subject}.ArealDistortion_MSMAll.native.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.BiasField_MSMAll.native.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.EdgeDistortion_MSMAll.native.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.L.ArealDistortion_MSMAll.native.shape.gii"
	files+=" ${check_dir}/${g_subject}.L.EdgeDistortion_MSMAll.native.shape.gii"
	files+=" ${check_dir}/${g_subject}.L.sphere.MSMAll.native.surf.gii"
	files+=" ${check_dir}/${g_subject}.MyelinMap_BC_MSMAll.native.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.native.wb.spec"
	files+=" ${check_dir}/${g_subject}.R.ArealDistortion_MSMAll.native.shape.gii"
	files+=" ${check_dir}/${g_subject}.R.EdgeDistortion_MSMAll.native.shape.gii"
	files+=" ${check_dir}/${g_subject}.R.sphere.MSMAll.native.surf.gii"
	files+=" ${check_dir}/${g_subject}.SmoothedMyelinMap_BC_MSMAll.native.dscalar.nii"

	functional_scans=`ls -d ${archiveDir}/RESOURCES/*fMRI*_preproc`
	for functional_scan in ${functional_scans} ; do

		#echo "functional_scan: ${functional_scan}"
		functional_scan_name=${functional_scan##*/}
		#echo "functional_scan_name: ${functional_scan_name}"
		functional_scan_name=${functional_scan_name%_preproc}
		#echo "functional_scan_name: ${functional_scan_name}"


		check_dir="${msm_all_dedrift_resource_dir}/MNINonLinear/Results/${functional_scan_name}"

		files+=" ${check_dir}/${functional_scan_name}_Atlas_MSMAll.dtseries.nii"
		files+=" ${check_dir}/${functional_scan_name}_MSMAll.L.atlasroi.32k_fs_LR.func.gii"
		files+=" ${check_dir}/${functional_scan_name}_MSMAll.R.atlasroi.32k_fs_LR.func.gii"
		files+=" ${check_dir}/${functional_scan_name}_s2_MSMAll.L.atlasroi.32k_fs_LR.func.gii"
		files+=" ${check_dir}/${functional_scan_name}_s2_MSMAll.R.atlasroi.32k_fs_LR.func.gii"

		is_resting_state=`echo "${functional_scan_name}" | grep "REST"`
		#echo "functional_scan_name: ${functional_scan_name}"
		#echo "is_resting_state: ${is_resting_state}"

		if [ "${is_resting_state}" != "" ] ; then
			files+=" ${check_dir}/${functional_scan_name}_Atlas_MSMAll_hp2000_clean.dtseries.nii"
			check_dir+="/${functional_scan_name}_hp2000.ica"
			files+=" ${check_dir}/Atlas.dtseries.nii"
			files+=" ${check_dir}/Atlas_hp_preclean.dtseries.nii"
			files+=" ${check_dir}/mc/prefiltered_func_data_mcf.par"
		fi
	done

	check_dir="${msm_all_dedrift_resource_dir}/T1w/fsaverage_LR32k"

	files+=" ${check_dir}/${g_subject}.L.inflated_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.L.midthickness_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.L.midthickness_MSMAll_va.32k_fs_LR.shape.gii"
	files+=" ${check_dir}/${g_subject}.L.pial_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.L.very_inflated_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.L.white_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.midthickness_MSMAll_va.32k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.midthickness_MSMAll_va_norm.32k_fs_LR.dscalar.nii"
	files+=" ${check_dir}/${g_subject}.MSMAll.32k_fs_LR.wb.spec"
	files+=" ${check_dir}/${g_subject}.R.inflated_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.R.midthickness_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.R.midthickness_MSMAll_va.32k_fs_LR.shape.gii"
	files+=" ${check_dir}/${g_subject}.R.pial_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.R.very_inflated_MSMAll.32k_fs_LR.surf.gii"
	files+=" ${check_dir}/${g_subject}.R.white_MSMAll.32k_fs_LR.surf.gii"

	check_dir="${msm_all_dedrift_resource_dir}/T1w/Native"
	files+=" ${check_dir}/${g_subject}.native.wb.spec"

	all_files_exist="TRUE"
	for filename in ${files} ; do
			
		if [ ! -e "${filename}" ] ; then
			all_files_exist="FALSE"

			if [ "${g_details}" = "TRUE" ]; then
				echo "Does not exist: ${filename}"
			fi
		fi
	done

	echo -e "\tResource Exists: ${resource_exists}\tFiles Exist: ${all_files_exist}"
}

main $@
