#!/bin/bash

python getPipelineResources.py \
    -U tbbrown \
    -P  \
    -WS https://db.humanconnectome.org \
    -PPL structural \
    -Prj HCP_Staging \
    -D . \
    -F batch11.out \
    -S "979984,983773,984472,987983,991267,992774,994273"



