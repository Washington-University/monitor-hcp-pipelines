#!/bin/bash

#~ND~FORMAT~MARKDOWN
#~ND~START~
#
# # CheckForOtherSubjectsData
#
# ## Script Description
# 
# This script performs a search for files in the archive directory for a specified subject
# for which the file name contains a subject number (any 6 digit number) but that subject
# number doesn't match the specified subject.
#
# For example, if the subject specified to check for this script is 1266628 and the project
# specified is HCP_Staging, this script will look in the archive directory 
#
#   /data/hcpdb/archive/HCP_Staging/arc001/126628_3T 
#
# for all files that contain a 6 digit number in their filename, but that 6 digit number
# is not 126628.
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
ARCHIVE_ROOT="/data/hcpdb/archive"
ARCHIVE_PROJ_SUBDIR="arc001"
TESLA_SPEC="_3T"

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
    echo "  Search for files in the archive for a specified subject and project that have"
    echo "  an apparent subject number in the file name that doesn't match the specified"
    echo "  subject"
    echo ""
    echo "  Usage: ${scriptName} <options>"
    echo ""
    echo "  Options: [ ] = optional; < > = user supplied value"
    echo ""
    echo "    [--help]  : show usage information and exit"
    echo ""
    echo "    [--debug] : show debugging information on stderr"
    echo ""
    echo "    --project <project-name> | --project=<project-name>"
    echo "    : name of project to check"
    echo ""
    echo "    --subject <subject-id> | --subject=<subject-id>"
    echo "    : ID of subject to check"
    echo ""
    echo "  Output: (stdout)"
    echo ""
    echo "    List of filenames that appear to indicate they are not for the subject specified"
    echo "    but are in that subject's archive"
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
#  ${projectName}  = User specified project name
#  ${subjectId}    - User specified subject id
#
get_options() {
    local arguments=($@)

    # initialize global output variables
    unset debug
    unset projectName
    unset subjectId

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
            --project)
                projectName=${arguments[$(( index + 1 ))]}
                index=$(( index + 2 ))
                ;;
            --project=*)
                projectName=${argument/*=/""}
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
            *)
                echo "Unrecognized Option: ${argument}"
                usage
                exit 1
                ;;
        esac
    done

    # check required parameters
    if [ -z ${projectName} ]; then
        usage
        echo ""
        echo "ERROR: <project-name> is required."
        echo ""
        exit 1
    fi

    if [ -z ${subjectId} ]; then
        usage
        echo ""
        echo "ERROR: <subject-id> is required."
        echo ""
        exit 1
    fi

    # report options
    debugEcho "${FUNCNAME}: projectName: ${projectName}"
    debugEcho "${FUNCNAME}: subjectId: ${subjectId}"
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
    #  ${projectName}  = User specified project name
    #  ${subjectId}    - User specified subject id
    get_options $@

    presentDir=`pwd`
    archiveDir="${ARCHIVE_ROOT}/${projectName}/${ARCHIVE_PROJ_SUBDIR}/${subjectId}${TESLA_SPEC}"

    cd ${archiveDir}
    find . -print | grep '[0-9]\{6,6\}' | grep -v ${subjectId} 
}

#
# Invoke the main function to get things started
#
main $@
