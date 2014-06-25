subj=${1}

echo "Checking subject: ${subj}"
../CheckForOtherSubjectsData.sh --project=HCP_Staging --subject=${subj} | tee ${subj}.out

more ${subj}.out


