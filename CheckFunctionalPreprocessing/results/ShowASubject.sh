#!/bin/bash

file="${1}".out

echo ""
echo " Look at date:"
echo ""
ls -l ${file}

echo ""
echo " grep for FAIL"
grep -i FAIL ${file}
echo ""
echo ""


