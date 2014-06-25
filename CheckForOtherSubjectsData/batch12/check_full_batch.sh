subjectList="126931 129432 143527 197449 745555"

for subj in ${subjectList} ; do
    echo "Checking subject: ${subj}"
    ../CheckForOtherSubjectsData.sh --project=HCP_Staging --subject=${subj} | tee ${subj}.out
done
