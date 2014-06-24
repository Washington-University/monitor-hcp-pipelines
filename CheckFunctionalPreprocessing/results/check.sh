../CheckFunctionalPreprocessing.sh --project=HCP_Staging --subjects=${1} | tee ${1}.out | grep FAIL
