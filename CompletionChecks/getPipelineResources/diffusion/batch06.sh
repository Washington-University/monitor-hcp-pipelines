#!/bin/bash

python ../getPipelineResources.py \
    -U tbbrown \
    -P \
    -WS https://db.humanconnectome.org \
    -PPL diffusion \
    -Prj HCP_Staging \
    -D . \
    -F batch06.out \
    -S "199655,199958,200109,200614,201111,201414,201818,203418,204016,204521,205119,205220,205725,205826,207628,208024,208226,208327,209733,209834,209935,210011,210415,210617,211316,211417,211720,211922,212116,212217,212318,212419,214019,214221,214423,214726,217126,217429,219231,221319,224022,233326,239944,245333,246133,249947,250427"

# 199554 - Review existing packaged data to assess need to re-recon second functional session, which did not use final recon version - no MR session built
# 201717 - head coil dropout issue - no MR session built
# 208428 - "" - but "volumes and surfaces look OK, per Erin