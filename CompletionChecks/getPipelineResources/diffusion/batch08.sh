#!/bin/bash

python ../getPipelineResources.py \
    -U tbbrown \
    -P  \
    -WS https://db.humanconnectome.org \
    -PPL diffusion \
    -Prj HCP_Staging \
    -D . \
    -F batch08.out \
    -S "441939,445543,448347,465852,467351,473952,475855,479762,480141,485757,486759,497865,499566,500222,510326,519950,521331,522434,528446,530635,531536,540436,541640,541943,545345,547046,552544,559053,561242,562446,565452,566454,567052,567961,568963,570243,573249,573451,579665,580044,580347,581349,583858,585862,586460,592455,594156,598568,599065"

# 571548 - head coil drop issue
# 467351 - Review existing packaged data to assess need to re-recon second functional session, which did not use final recon version.