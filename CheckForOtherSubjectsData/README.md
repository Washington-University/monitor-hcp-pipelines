# CheckForOtherSubjectsData

## Description

Performs a search for files in the archive directory for a specified subject
for which the file name contains a subject number (in this case any 6 digit number)
but that subject number doesn't match the specified subject.

Early in the pipeline processing for the [Human Connectome Project][HCP] (HCP) 
500 subject release there was a problem in which attempting to run structural
preprocessing on a subject for which there was no existing session somehow caused
data files named for that subject to show up in the resources for other subjects.

This script was written to detect when the cases in which that problem occurred.

<!-- References -->
[HCP]: http://www.humanconnectome.org
