#!/bin/bash

python ../getPipelineResources.py \
    -U tbbrown \
    -P \
    -WS https://db.humanconnectome.org \
    -PPL diffusion \
    -Prj HCP_Staging \
    -D . \
    -F TestBatchOf3.out \
    -S "105014,100307,142828"
