subj="${1}"

if [ -z "${subj}" ] ; then
    printf "Subject: " 
    read subj
fi

echo "Checking subject: ${subj}"
../CheckFunctionalPreprocessing.sh --project=HCP_Staging --subjects=${subj} | tee ${subj}.out | grep FAIL
