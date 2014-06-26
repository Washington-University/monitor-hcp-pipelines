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
PREPROCESSING_PACKAGE_DIR="preproc"
didAnyTestsFail="False"
PREPROC_PACKAGE_TYPES="Structural rfMRI_REST1 rfMRI_REST2 tfMRI_EMOTION tfMRI_GAMBLING tfMRI_LANGUAGE tfMRI_MOTOR tfMRI_RELATIONAL tfMRI_SOCIAL tfMRI_WM Diffusion"

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
    echo " Note:"
    echo ""
    echo "   The following package related files are checked: "
    local aPackageType
    for aPackageType in ${PREPROC_PACKAGE_TYPES} ; do
        echo "    <subject-id>_3T_${aPackageType}_preproc.zip" 
        echo "    <subject-id>_3T_${aPackageType}_preproc.zip.md5" 
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
    echo "Subject Package Directory: ${subjectPackageDir}"
    echo -e "package file:\tExists\tChecksum Exists\tChecksum correct"

    for packageType in ${PREPROC_PACKAGE_TYPES}; do
        
        packageFileName="${subjectPackageDir}/${subjectId}_3T_${packageType}_preproc.zip"
        packageCheckSumFileName="${packageFileName}.md5"

        # check for package file existence
        testDesc="${packageFileName##*/}"
        
        if [ -e ${packageFileName} ]; then
            packageFileExists="True"
        else
            packageFileExists="False"
        fi

        # check for checksum file existence
        if [ -e ${packageCheckSumFileName} ]; then
            checksumFileExists="True"
        else
            checksumFileExists="False"
        fi

        # check the checksum value
        if [ "${packageFileExists}" = "True" ] && [ "${checksumFileExists}" = "True" ]; then
            tmpFile=`mktemp`
            md5sum ${packageFileName} | cut -d' ' -f1 > ${tmpFile}.1
            cat ${packageCheckSumFileName} | cut -d' ' -f1 > ${tmpFile}.2
            
            if diff ${tmpFile}.1 ${tmpFile}.2 > /dev/null; then
                checkSumsEquivalent="True"
            else
                checkSumsEquivalent="False"
            fi

            rm -f ${tmpFile}.1
            rm -f ${tmpFile}.2
        else
            checkSumsEquivalent="False"
        fi

        # output information
        echo -e "${testDesc}:\t${packageFileExists}\t${checksumFileExists}\t${checkSumsEquivalent}"

        if [ "${packageFileExists}" != "True" ] || [ "${checksumFileExists}" != "True" ] || [ "${checkSumsEquivalent}" != "True" ]; then
            didAnyTestsFail="True"
        fi
    done
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

