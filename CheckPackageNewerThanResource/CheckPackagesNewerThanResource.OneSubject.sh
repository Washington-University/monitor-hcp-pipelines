#!/bin/bash

PACKAGING_ROOT="/data/hcpdb/packages/prerelease/zip"
ARCHIVE_ROOT="/data/hcpdb/archive"


get_options() {
    local arguments=($@)

    # initialize global output variables
    unset g_subject
	unset g_project

    # parse arguments
    local index=0
    local numArgs=${#arguments[@]}
    local argument

    while [ ${index} -lt ${numArgs} ]; do
        argument=${arguments[index]}

        case ${argument} in
            --subject=*)
                g_subject=${argument/*=/""}
                index=$(( index + 1 ))
                ;;
            --project=*)
                g_project=${argument/*=/""}
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
    if [ -z "${g_subject}" ]; then
        echo ""
        echo "ERROR: --subject=<subject-id> is required."
        echo ""
        exit 1
    fi

	if [ -z "${g_project}" ]; then
        echo ""
        echo "ERROR: --project=<project-id> is required."
        echo ""
        exit 1
    fi
}

get_date()
{
	local path=${1}
	local __functionResultVar=${2}
	local file_info
	local the_date

	if [ -e "${path}" ] ; then
		file_info=`ls -lhd ${path}`
		the_date=`echo ${file_info} | cut -d " " -f 6-8`
	else
		the_date="DOES NOT EXIST"
	fi

	eval $__functionResultVar="'${the_date}'"
}


check_structural_preproc_packages()
{
	local resource_dir="${ARCHIVE_ROOT}/${g_project}/arc001/${g_subject}_3T/RESOURCES/Structural_preproc"

	local package_dir="${PACKAGING_ROOT}/${g_project}/${g_subject}/preproc"
	local package_files=""
	package_files+="${package_dir}/${g_subject}_3T_Structural_preproc.zip "
	package_files+="${package_dir}/${g_subject}_3T_Structural_preproc_extended.zip "

	for package_file in ${package_files} ; do

		if [ -e "${package_file}" ] ; then

			local resource_date
			local package_date
			get_date ${resource_dir} resource_date
			get_date ${package_file} package_date

			if [[ "${resource_dir}" -nt "${package_file}" ]]; then				
				echo ""
				echo "--ERROR-- --Subject-- ${g_subject}"
				echo -e "\tresource_dir: ${resource_dir}\t${resource_date}\tpackage_file: ${package_file}\t${package_date} -- ERROR"
				echo "--ERROR-- resource date: ${resource_date} is newer than package date: ${package_date}"
				echo ""
			else
				echo -e "package_file: ${package_file} -- OK"
			fi

		fi

	done
}

check_diffusion_preproc_packages()
{
	local resource_dir="${ARCHIVE_ROOT}/${g_project}/arc001/${g_subject}_3T/RESOURCES/Diffusion_preproc"

	local package_dir="${PACKAGING_ROOT}/${g_project}/${g_subject}/preproc"
	local package_files=""
	package_files+="${package_dir}/${g_subject}_3T_Diffusion_preproc.zip "

	for package_file in ${package_files} ; do

		if [ -e "${package_file}" ] ; then

			local resource_date
			local package_date
			get_date ${resource_dir} resource_date
			get_date ${package_file} package_date

			if [[ "${resource_dir}" -nt "${package_file}" ]]; then
				echo ""
				echo "--ERROR-- --Subject-- ${g_subject}"
				echo -e "\tresource_dir: ${resource_dir}\t${resource_date}\tpackage_file: ${package_file}\t${package_date} -- ERROR"
				echo "--ERROR-- resource date: ${resource_date} is newer than package date: ${package_date}"
				echo ""
			else
				echo -e "package_file: ${package_file} -- OK"
			fi

		fi	

	done
}


check_functional_preproc_packages()
{
	local func_scans=""
	func_scans+="rfMRI_REST1 "
	func_scans+="rfMRI_REST2 "
	func_scans+="tfMRI_EMOTION "	
	func_scans+="tfMRI_GAMBLING "
	func_scans+="tfMRI_LANGUAGE "
	func_scans+="tfMRI_MOTOR "
	func_scans+="tfMRI_RELATIONAL "
	func_scans+="tfMRI_SOCIAL "
	func_scans+="tfMRI_WM "

	for func_scan in ${func_scans} ; do

		for direction in LR RL ; do 

			local resource_dir="${ARCHIVE_ROOT}/${g_project}/arc001/${g_subject}_3T/RESOURCES/${func_scan}_${direction}_preproc"

			local package_dir="${PACKAGING_ROOT}/${g_project}/${g_subject}/preproc"
			local package_files=""
			package_files+="${package_dir}/${g_subject}_3T_${func_scan}_preproc.zip "

			for package_file in ${package_files} ; do
				
				local resource_date
				local package_date
				get_date ${resource_dir} resource_date
				get_date ${package_file} package_date
				
				if [[ "${resource_dir}" -nt "${package_file}" ]]; then
					echo ""
					echo "--ERROR-- --Subject-- ${g_subject}"
					echo -e "\tresource_dir: ${resource_dir}\t${resource_date}\tpackage_file: ${package_file}\t${package_date} -- ERROR"
					echo "--ERROR-- resource date: ${resource_date} is newer than package date: ${package_date}"
					echo ""
				else
					echo -e "package_file: ${package_file} -- OK"
				fi

			done

		done

	done
}


check_fix_package()
{
	local rest_scans=""
	rest_scans+="rfMRI_REST1 "
    rest_scans+="rfMRI_REST2 "

	for rest_scan in ${rest_scans} ; do

		for direction in LR RL ; do 

			local resource_dir="${ARCHIVE_ROOT}/${g_project}/arc001/${g_subject}_3T/RESOURCES/${rest_scan}_${direction}_FIX"

			local package_dir="${PACKAGING_ROOT}/${g_project}/${g_subject}/fix"
			local package_files=""
			package_files+="${package_dir}/${g_subject}_3T_rfMRI_REST_fix.zip "

			for package_file in ${package_files} ; do
				
				local resource_date
				local package_date
				get_date ${resource_dir} resource_date
				get_date ${package_file} package_date
				
				if [[ "${resource_dir}" -nt "${package_file}" ]]; then
					echo ""
					echo "--ERROR-- --Subject-- ${g_subject}"
					echo -e "\tresource_dir: ${resource_dir}\t${resource_date}\tpackage_file: ${package_file}\t${package_date} -- ERROR"
					echo "--ERROR-- resource date: ${resource_date} is newer than package date: ${package_date}"
					echo ""
				else
					echo -e "package_file: ${package_file} -- OK"
				fi

			done

		done

	done
}

check_fix_extended_packages()
{
	local rest_scans=""
	rest_scans+="rfMRI_REST1 "
    rest_scans+="rfMRI_REST2 "

	for rest_scan in ${rest_scans} ; do

		for direction in LR RL ; do 

			local resource_dir="${ARCHIVE_ROOT}/${g_project}/arc001/${g_subject}_3T/RESOURCES/${rest_scan}_${direction}_FIX"

			local package_dir="${PACKAGING_ROOT}/${g_project}/${g_subject}/fixextended"
			local package_files=""
			package_files+="${package_dir}/${g_subject}_3T_${rest_scan}_fixextended.zip "

			for package_file in ${package_files} ; do
				
				local resource_date
				local package_date
				get_date ${resource_dir} resource_date
				get_date ${package_file} package_date
				
				if [[ "${resource_dir}" -nt "${package_file}" ]]; then
					echo ""
					echo "--ERROR-- --Subject-- ${g_subject}"
					echo -e "\tresource_dir: ${resource_dir}\t${resource_date}\tpackage_file: ${package_file}\t${package_date} -- ERROR"
					echo "--ERROR-- resource date: ${resource_date} is newer than package date: ${package_date}"
					echo ""
				else
					echo -e "package_file: ${package_file} -- OK"
				fi

			done

		done

	done
}

check_task_packages()
{
	local smoothing_levels=""
	smoothing_levels+="2 "
	smoothing_levels+="4 "
	smoothing_levels+="8 "
	smoothing_levels+="12 "
	
	for smoothing_level in ${smoothing_levels} ; do
		
		local task_scans=""
		task_scans+="tfMRI_EMOTION "	
		task_scans+="tfMRI_GAMBLING "
		task_scans+="tfMRI_LANGUAGE "
		task_scans+="tfMRI_MOTOR "
		task_scans+="tfMRI_RELATIONAL "
		task_scans+="tfMRI_SOCIAL "
		task_scans+="tfMRI_WM "
		
		for task_scan in ${task_scans} ; do
			
			local resource_dir="${ARCHIVE_ROOT}/${g_project}/arc001/${g_subject}_3T/RESOURCES/${task_scan}"
			
			local package_dir="${PACKAGING_ROOT}/${g_project}/${g_subject}/analysis_s${smoothing_level}"
			local package_files=""
			package_files+="${package_dir}/${g_subject}_3T_${task_scan}_analysis_s${smoothing_level}.zip "
			
			for package_file in ${package_files} ; do
				
				local resource_date
				local package_date
				get_date ${resource_dir} resource_date
				get_date ${package_file} package_date
				
				if [[ "${resource_dir}" -nt "${package_file}" ]]; then
					echo ""
					echo "--ERROR-- --Subject-- ${g_subject}"
					echo -e "\tresource_dir: ${resource_dir}\t${resource_date}\tpackage_file: ${package_file}\t${package_date} -- ERROR"
					echo "--ERROR-- resource date: ${resource_date} is newer than package date: ${package_date}"
					echo ""
				else
					echo -e "package_file: ${package_file} -- OK"
				fi

			done
			
		done
		
	done
}

main() 
{
	get_options $@

	check_structural_preproc_packages

	check_diffusion_preproc_packages

	check_functional_preproc_packages

	check_fix_package

	check_fix_extended_packages

	check_task_packages
}

#
# Invoke the main function to get things started
#
main $@


