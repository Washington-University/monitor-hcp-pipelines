#!/bin/bash

python ../getPipelineResources.py \
    -U tbbrown \
    -P \
    -WS https://db.humanconnectome.org \
    -PPL diffusion \
    -Prj HCP_Staging \
    -D . \
    -F batch04.out \
    -S "158035,158136,158540,159138,159239,159340,159441,160123,160830,161731,162026,162228,162329,162733,163129,163331,163432,163836,164030,164131,164939,165032,165840,167036,167743,168139,168341,169343,169444,170934,171431,171633,172029,172130,172332,172534,173132,173334,173435,173536,173940,175035,175439,176542,177645"

# 161327 - head coil issue, no MR session built yet
# 165234 - head coil issue, no MR session built yet
# 169141 - head coil issue, no MR session built yet
# 172231 - excluded (Neurospecial) subject, no MR session built
# 175540 - review existing package data to assess need to re-recon second functional session, which did not use final recon version - no MR session built