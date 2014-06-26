#!/bin/bash

file="${1}".out

echo ""
echo " Look at date:"
echo ""
ls -l ${file}

echo ""
echo " Look for false:"
echo ""
cat ${file}

echo ""
echo " grep for false:"
grep -i false ${file}
echo ""
echo ""


