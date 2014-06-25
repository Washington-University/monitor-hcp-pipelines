subjectList="142424 165234 169141"

for subj in ${subjectList} ; do
    echo "Checking subject: ${subj}"
    ../CheckForOtherSubjectsData.sh --project=HCP_Staging --subject=${subj} | tee ${subj}.out
done
