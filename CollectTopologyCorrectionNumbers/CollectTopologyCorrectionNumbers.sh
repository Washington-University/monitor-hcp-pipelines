#!/bin/bash

#
# Description:
#  Global variables
#
PROVENANCE_ARCHIVE_ROOT="/home/shared/NRG/hcp_shared/ProvenanceArchive"

#
# Function Description:
#  Show usage information for this script
#
usage() {
    local scriptName=$(basename ${0})
    echo ""
    echo "Program Information:"
    echo ""
    echo "  Collect ..."
    echo ""
    echo "Usage: ${scriptName} <options>"
    echo ""
    echo "  Options: [ ] = optional; < > = user supplied value"
    echo ""
    echo "    [--help]  : show this usage information and exit"
    echo ""
    echo "    --project <project-spec> | --project=<project-spec>"
    echo "    : specification of project on which to work"
    echo ""
}

#
# Function Description:
#  Get the command line options for this script.
#  Shows usage information and exits if the command 
#  line is malformed.
#
# Global Output Variables:
#  ${project}      - project specification
#
get_options() {
    local arguments=($@)
    
    # initialize global output variables
    unset project
    
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
            --project)
                project=${arguments[$(( index + 1 ))]}
                index=$(( index + 2 ))
                ;;
            --project=*)
                project=${argument/*=/""}
                index=$(( index + 1 ))
                ;;
            *)
                echo "Unrecognized Option: ${argument}"
                usage
                exit 1
                ;;
        esac
    done

    if [ -z "$project" ]; then
        usage
        echo ""
        echo "ERROR: <project-spec> REQUIRED BUT NOT SPECIFIED"
        echo ""
        exit 1
    fi

    # report options
    echo "project: ${project}"
}

#
# Function Description:
#  Main processing of script.
#
main() {
    # Get Command Line Options
    #
    # Global Variables Set:
    #  ${project}      - project specification
    get_options $@

    rootDir="${PROVENANCE_ARCHIVE_ROOT}/data/hcpdb/archive/${project}/arc001"
    subjectDirs=`ls -d ${rootDir}/*`

    echo -e "Total Defects\tAverage Vertex Count"
    
    for subjectDir in ${subjectDirs}; do
        #echo ""
        #echo "============================="
        #curDate=`date`
        #echo "${curDate}: SUBJECT DIRECTORY: ${subjectDir}"
        #echo "============================="
        #echo ""

        resourceDir="${subjectDir}/RESOURCES"
        structuralPreprocDir="${resourceDir}/Structural_preproc"
        structuralLogFile="${structuralPreprocDir}/StructuralHCP.log"

        if [ -f ${structuralLogFile} ] ; then
            curDate=`date`
            #echo -e "${curDate}:\tFound structural log file: ${structuralLogFile}"
            tempFile="/tmp/$(basename $0).$$.tmp"
            grep "CORRECTING DEFECT" ${structuralLogFile} > ${tempFile}

            defectCount=0
            totalVertexCount=0

            while read line; do
                defectNumber=`echo "${line}" | awk '{print $3}'`
                
                vertexField=`echo "${line}" | awk '{print $4}'`
                vertexField=${vertexField##*=}
                vertexCount=${vertexField%%,*}
                
                #echo "defectNumber: ${defectNumber}"
                #echo "vertextCount: ${vertexCount}"

                if [ ${defectNumber} = "0" ] ; then
                    
                    if [ ${defectCount} != "0" ]; then
                        totalDefects=${defectCount}
                        averageVertexCount=$(( totalVertexCount / totalDefects ))
                        echo -e "${totalDefects}\t${averageVertexCount}"
                    fi
                    
                    defectCount=1
                    totalVertexCount="${vertexCount}"
                else
                    defectCount=$(( defectCount + 1 ))
                    totalVertexCount=$(( totalVertexCount + vertexCount ))
                fi
                
            done < ${tempFile}
            rm ${tempFile}
            
            totalDefects=${defectCount}
            averageVertexCount=$(( totalVertexCount / totalDefects ))
            echo -e "${totalDefects}\t${averageVertexCount}"
        fi
    done
    
    curDate=`date`
    echo "${curDate}: FINISHED"
}

#
# Invoke the main function to get things started
#
main $@

