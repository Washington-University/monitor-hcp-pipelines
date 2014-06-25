subjectList="979984 983773 984472 987983 991267 992774 994273"

for subj in ${subjectList} ; do
    echo "Checking subject: ${subj}"
    ../CheckForOtherSubjectsData.sh --project=HCP_Staging --subject=${subj} | tee ${subj}.out
done
