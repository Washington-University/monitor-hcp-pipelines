subj="${1}"

echo "Checking subject: ${subj}"
../CheckFunctionalPreprocessing.sh --project=HCP_Staging --subjects=${subj} | tee ${subj}.out | grep FAIL
