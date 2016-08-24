#!/bin/bash

#~ND~FORMAT~MARKDOWN
#~ND~START~
#
# # Check Package Existence
#
# ## Description
# 
# This script performs a series of checks to determine whether
# appropriate package files exist for a specified subject.
#
# ## Script Assumptions
#
#  * 
#
# ## Author(s)
#
#  * Timothy B. Brown (tbbrown at wustl dot edu)
#
#~ND~END~

#
# Description:
#  Global variables 
#
DEFAULT_PACKAGING_ROOT="/data/hcpdb/packages/prerelease/zip"
didAnyTestsFail="False"

PREPROCESSING_PACKAGE_DIR="preproc"
PREPROC_PACKAGE_TYPES="Structural rfMRI_REST1 rfMRI_REST2 tfMRI_EMOTION tfMRI_GAMBLING tfMRI_LANGUAGE tfMRI_MOTOR tfMRI_RELATIONAL tfMRI_SOCIAL tfMRI_WM Diffusion"
PREPROC_EXTENDED_PACKAGE_TYPES="Structural_preproc_extended"

FIX_PACKAGE_DIR="fix"
FIX_PACKAGE_TYPES="rfMRI_REST"

FIX_EXTENDED_PACKAGE_DIR="fixextended"
FIX_EXTENDED_PACKAGE_TYPES="rfMRI_REST1 rfMRI_REST2"

TASK_ANALYSIS_SMOOTHING_LEVELS="2 4 8 12"
TASK_ANALYSIS_PACKAGE_TYPES="tfMRI_EMOTION tfMRI_GAMBLING tfMRI_LANGUAGE tfMRI_MOTOR tfMRI_RELATIONAL tfMRI_SOCIAL tfMRI_WM" 

#
# Function Description:
#  Echo output to stderr if in debugging mode
#  (i.e. if the debug variable is set to True)
#
debugEcho() {
    if [ "${debug}" = "True" ]; then
        echo "Debug: $@" 1>&2 
    fi
}

# 
# Function Description:
#  Show usage information for this script
#
usage() {
    local scriptName=$(basename ${0})
    echo ""
    echo "  Perform a series of checks to determine whether appropriate"
    echo "  package files exist for a specified subject. It also regenerates"
    echo "  the checksum for the package file and compares it to the contents"
    echo "  of the package's checksum file."
    echo ""
    echo "  Usage: ${scriptName} <options>"
    echo ""
    echo "  Options: [ ] = optional; < > = user supplied value"
    echo ""
    echo "    [--help]  : show this usage information and exit"
    echo ""
    echo "    [--debug] : show debugging information on stderr"
    echo ""
    echo "    --subject <subject-id> | --subject=<subject-id>"
    echo "    : ID of subject to check"
    echo ""
    echo "    [--rootdir <packaging-root> | --rootdir=<packaging-root>]"
    echo "    : path to root directory for checking for packages"
    echo "      If unspecified, ${DEFAULT_PACKAGING_ROOT} will be used."
    echo "      Preprocessing packages will be checked for at: "
    echo "      <packaging-root>/<subject-id>/${PREPROCESSING_PACAKGE_DIR}"
    echo ""
	echo "    [--suppress-checksum-regen]"
	echo "    : if specified, then the checksum regeneration check will"
	echo "      not be done"
	echo ""
    echo " Note:"
    echo ""
    echo "   The following preproc package related files are checked: "
    local aPackageType
    for aPackageType in ${PREPROC_PACKAGE_TYPES} ; do
        echo "    <subject-id>_3T_${aPackageType}_preproc.zip" 
        echo "    <subject-id>_3T_${aPackageType}_preproc.zip.md5" 
    done

	echo "   The following preproc extended package related files are checked: "
	for aPackageType in ${PREPROC_EXTENDED_PACKAGE_TYPES} ; do 
		echo "    <subject-id>_3T_${aPackageType}.zip"
		echo "    <subject-id>_3T_${aPackageType}.zip.md5"
	done

    echo ""
    echo "   The following fix package related files are checked: "
    for aPackageType in ${FIX_PACKAGE_TYPES} ; do
        echo "    <subject-id>_3T_${aPackageType}_fix.zip"
        echo "    <subject-id>_3T_${aPackageType}_fix.zip.md5"
    done
    echo ""
    echo "  Output: (stdout)"
    echo ""
    echo "    For each package file checked for, a True/False indication of the files existence,"
    echo "    a True/False indication of a corresponding checksum file existence, and a True/False"
    echo "    indication of the checksum's correctness is output"
    echo ""
    echo "  Return Code:"
    echo ""
    echo "    0 if help was not requested, all parameters were properly formed, and all"
    echo "      tests performed passed"
    echo "    1 otherwise - malformed parameters, help requested, or at least one test"
    echo "      failed"
    echo ""
}

#
# Function Description:
#  Get the command line options for this script.
#  Shows usage information an exits if command line 
#  is malformed.
#
# Global Output Variables:
#  ${debug}        - Set to "True" if user has requested debugging information
#  ${subjectId}    - User specified subject id
#  ${rootDir}      - path to root packaging directory
#
get_options() {
    local arguments=($@)

    # initialize global output variables
    unset debug
    unset subjectId
    rootDir=${DEFAULT_PACKAGING_ROOT}
	g_suppress_checksum_regen="FALSE"

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
            --debug)
                debug="True"
                index=$(( index + 1 ))
                ;;
            --subject)
                subjectId=${arguments[$(( index + 1 ))]}
                index=$(( index + 2 ))
                ;;
            --subject=*)
                subjectId=${argument/*=/""}
                index=$(( index + 1 ))
                ;;
            --rootdir)
                rootDir=${arguments[$(( index + 1 ))]}
                index=$(( index + 2 ))
                ;;
            --rootdir=*)
                rootDir=${argument/*=/""}
                index=$(( index + 1 ))
                ;;
            --suppress-checksum-regen)
                g_suppress_checksum_regen="TRUE"
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
    if [ -z ${subjectId} ]; then
        usage
        echo ""
        echo "ERROR: <subject-id> is required."
        echo ""
        exit 1
    fi

    # report options
    debugEcho "${FUNCNAME}: subjectId: ${subjectId}"
    debugEcho "${FUNCNAME}: rootDir: ${rootDir}"
	debugEcho "${FUNCNAME}: g_suppress_checksum_regen: ${g_suppress_checksum_regen}"
}

get_date()
{
	local path=${1}
	local __functionResultVar=${2}
	local file_info
	local the_date

	if [ -e "${path}" ] ; then
		file_info=`ls -lh ${path}`
		the_date=`echo ${file_info} | cut -d " " -f 6-8`
	else
		the_date="DOES NOT EXIST"
	fi

	eval $__functionResultVar="'${the_date}'"
}

#
# Function Description:
#  TBW
#
check_package_file() {
    local arguments=($@)
    local packageFileName=${arguments[0]}

    local packageCheckSumFileName="${packageFileName}.md5"
    local packageFileExists="False"
	local packageFileSize="N/A"
    local checksumFileExists="False"
    local tmpFile=""
    local checkSumsEquivalent="False"
	local subject=""

    # check for package file existence
    testDesc="${packageFileName##*/}"

	subject="${packageFileName%%_3T*}"
	subject="${subject##*/}"

    if [ -e ${packageFileName} ]; then
        packageFileExists="True"
		packageFileInfo=`ls -lh ${packageFileName}`
		packageFileSize=`echo ${packageFileInfo} | cut -d " " -f 5`
    fi

    # check for checksum file existence
    if [ -e ${packageCheckSumFileName} ]; then
        checksumFileExists="True"
    fi

    # check the checksum value
    if [ "${packageFileExists}" = "True" ] && [ "${checksumFileExists}" = "True" ]; then
		
		if [ "${g_suppress_checksum_regen}" = "TRUE" ] ; then
			checkSumsEquivalent="Not Checked"
		else
			tmpFile=`mktemp`
			md5sum ${packageFileName} | cut -d' ' -f1 > ${tmpFile}.1
			cat ${packageCheckSumFileName} | cut -d' ' -f1 > ${tmpFile}.2
            
			if diff ${tmpFile}.1 ${tmpFile}.2 > /dev/null; then
				checkSumsEquivalent="True"
			fi
			
			rm -f ${tmpFile}.1
			rm -f ${tmpFile}.2
		fi
	fi

	get_date ${packageFileName} package_date

    # output information
    echo -e "${subject}\t${testDesc}\t${packageFileExists}\t${packageFileSize}\t${checksumFileExists}\t${checkSumsEquivalent}\t${package_date}"

    # return success or failure indication
    if [ "${packageFileExists}" != "True" ] || [ "${checksumFileExists}" != "True" ] || [ "${checkSumsEquivalent}" != "True" ]; then
        return 1 # failure
    else
        return 0 # success
    fi
}

#
# Function Description:
#  Main processing of script.
#
#  Gets user specified command line options and runs tests
#
main() {
    # Get Command Line Options
    #
    # Global Variables Set:
    #  ${debug}        - Set to "True" if user has requested debugging information
    #  ${subjectId}    - User specified subject id
    #  ${rootDir}      - path to root packaging directory
    get_options $@

    subjectPackageDir="${rootDir}/${subjectId}/${PREPROCESSING_PACKAGE_DIR}"
    # echo "Subject Preprocessed Package Directory: ${subjectPackageDir}"

    subjectFixPackageDir="${rootDir}/${subjectId}/${FIX_PACKAGE_DIR}"
    # echo "Subject FIX Package Directory: ${subjectFixPackageDir}"

    subjectFixExtendedPackageDir="${rootDir}/${subjectId}/${FIX_EXTENDED_PACKAGE_DIR}"
    # echo "Subject FIX Extended Package Directory: ${subjectFixPackageDir}"

	# Header line
    #echo -e "subject\tpackage file\tExists\tSize\tChecksum Exists\tChecksum correct\tPackage Date"

    # check preproc packages
    for packageType in ${PREPROC_PACKAGE_TYPES}; do
        packageFileName="${subjectPackageDir}/${subjectId}_3T_${packageType}_preproc.zip"
        if ! check_package_file ${packageFileName} ; then
            didAnyTestsFail="True"
        fi
    done

	# check preproc extended packages
	for packageType in ${PREPROC_EXTENDED_PACKAGE_TYPES} ; do
		packageFileName="${subjectPackageDir}/${subjectId}_3T_${packageType}.zip"
		if ! check_package_file ${packageFileName} ; then
			didAnyTestsFail="True"
		fi
	done

    # # check fix packages
    # for packageType in ${FIX_PACKAGE_TYPES}; do
    #     packageFileName="${subjectFixPackageDir}/${subjectId}_3T_${packageType}_fix.zip"
    #     if ! check_package_file ${packageFileName} ; then
    #         didAnyTestsFail="True"
    #     fi
    # done

    # # check fixextended packages
    # for packageType in ${FIX_EXTENDED_PACKAGE_TYPES} ; do
    #     packageFileName="${subjectFixExtendedPackageDir}/${subjectId}_3T_${packageType}_fixextended.zip"
    #     if ! check_package_file ${packageFileName} ; then
    #         didAnyTestsFail="True"
    #     fi
    # done

    # # check task analysis packages
    # for smoothing_level in ${TASK_ANALYSIS_SMOOTHING_LEVELS} ; do

    #     subjectTaskAnalysisDir="${rootDir}/${subjectId}/analysis_s${smoothing_level}"
    #     # echo "Subject Task Analysis Package Directory: ${subjectTaskAnalysisDir}"
    #     # echo -e "package file:\tExists\tChecksum Exists\tChecksum correct"
    #     for packageType in ${TASK_ANALYSIS_PACKAGE_TYPES} ; do
    #         packageFileName="${subjectTaskAnalysisDir}/${subjectId}_3T_${packageType}_analysis_s${smoothing_level}.zip"
    #         if ! check_package_file ${packageFileName} ; then
    #             didAnyTestsFail="True"
    #         fi
    #     done

    # done
}

#
# Invoke the main function to get things started
#
main $@

if [ "${didAnyTestsFail}" = "True" ]; then
    exit 1
else
    exit 0
fi

