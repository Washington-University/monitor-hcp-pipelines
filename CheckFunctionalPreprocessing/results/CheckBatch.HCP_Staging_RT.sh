
#subjects=""
#subjects="${subjects} 105923 111312 114823 115320 125525 135528 144226 146129 149741 169343"
#subjects="${subjects} 172332 200109 200614 204521 287248 433839 562345 627549 877168"

#subjects=""
#subjects="${subjects} 103818 122317 137128 139839 143325 149337 151526 158035 175439 177746"
#subjects="${subjects} 185442 192439 194140 195041 599671 662551 783462 859671 861456"

subjects=""
subjects="${subjects} 187547 287248 341834 660951 "

project="HCP_Staging_RT"

for subject in $subjects ; do
    echo "Checking subject: ${subject}"
    ../CheckFunctionalPreprocessing.sh --project=${project} --subjects=${subject} | tee ${subject}.out | grep FAIL
done
