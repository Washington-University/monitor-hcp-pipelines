
subjectList="108323 151728 161327 161630 166438 172938 191336 194847 199554 208428 211215 231928 251833 339847 361941 382242 390645 571548 599469 749361 779370 792766 816653 957974 959069"

for subj in ${subjectList} ; do
    echo "Checking subject: ${subj}"
    ../CheckForOtherSubjectsData.sh --project=HCP_Staging --subject=${subj} | tee ${subj}.out
done
