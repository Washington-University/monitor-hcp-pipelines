
project="WU_L1A_Staging"

from_file=( $( cat ${project}.functional.subjects ) )
subjects="`echo "${from_file[@]}"`"

for subject in $subjects ; do
    echo "Checking subject: ${subject}"
    ../CheckFunctionalPreprocessing.sh --project=${project} --subjects=${subject} | tee ${subject}.out | grep FAIL
done
