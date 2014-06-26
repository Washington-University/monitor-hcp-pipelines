#!/bin/bash

python getPipelineResources.py \
    -U tbbrown \
    -P \
    -WS https://db.humanconnectome.org \
    -PPL fix \
    -Prj HCP_Staging \
    -D . \
    -F getPipelineResources.output.txt \
    -S "100307"
