
project="WU_L1B_Staging"

from_file=( $( cat ${project}.functional.subjects ) )
subjects="`echo "${from_file[@]}"`"

for subject in $subjects ; do
    echo "Checking subject: ${subject}"
    ../CheckFunctionalPreprocessing.sh \
        --project=${project} \
        --subjects=${subject} \
        --tasks="REST1,REST2,REST3,REST4,REST5,REST6,WM,GAMBLING,SOCIAL,EMOTION" | tee ${subject}.out | grep FAIL
done
