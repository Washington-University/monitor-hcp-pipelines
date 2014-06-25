# Collect Topology Correction Numbers

## Description

This script looks through the provenance archive for Structural_preproc resources
containing log files named StructuralHCP.log.

The StructuralHCP.log files are then searched for the phrase "CORRECTING DEFECT".
Each resulting line containing "CORRECTING DEFECT" is parsed for the defect
number and count of vertices in the defect. 

The total number of corrected defects for the log file is computed along with the 
average number of vertices in the defects for the log file.

For each log file, these two values (defect count and average vertex count) are
written to stdout (tab separated). The result can be imported into a spreadsheet
program (e.g. Excel) for further descriptive statistics calculation or processing.

This was done for use in comparison of the "average" number of topology corrections
done for the regular (normal, healthy adults) HCP data as compared to the LifeSpan
data which includes children and the elderly.

<!-- References -->
[HCP]: http://www.humanconnectome.org
