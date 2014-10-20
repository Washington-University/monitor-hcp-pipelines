
subjects=""
subjects="${subjects} LS2001 LS2003 LS2008 LS2009 LS2037 LS2043 LS3017 LS3019 LS3026 LS3029 "
subjects="${subjects} LS3040 LS3046 LS4025 LS4036 LS4041 LS4043 LS4047 LS5007 LS5038 LS5040 "
subjects="${subjects} LS5041 LS5049 LS6003 LS6006 LS6009 LS6038 LS6046 "

project="WU_L1A_Staging"

for subject in $subjects ; do
    echo "Checking subject: ${subject}"
    ../CheckFunctionalPreprocessing.sh --project=${project} --subjects=${subject} | tee ${subject}.out | grep FAIL
done
