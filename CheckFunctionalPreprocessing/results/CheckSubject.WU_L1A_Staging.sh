subj="${1}"

if [ -z "${subj}" ] ; then
    printf "Subject: " 
    read subj
fi

project="WU_L1A_Staging"

echo "Checking subject: ${subj}"
../CheckFunctionalPreprocessing.sh --project=${project} --subjects=${subj} | tee ${subj}.out | grep FAIL
