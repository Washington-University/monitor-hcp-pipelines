# monitor-hcp-pipelines

## Description

This repository contains various scripts for monitoring the completion of various
parts of the [Human Connectome Project][HCP] (HCP) Minimal Preprocessing Pipeline
(MPP).

Some of the checks performed by the scripts in this repository are simple checks
for "successful completion" of the various parts of the MPP (Structural Preprocessing,
Functional Preprocessing, Diffusion Preprocessing, ICA FIX processing, and Task fMRI 
Analysis). These checks are simply determine if appropriate database resources have
been created which indicate the completion of the various parts of the MPP and for
each resource the existence of a few select files is checked as a further indication
of the "successful" completion of the indicated type of processing. 

Other checks performed by the scripts in this repository can be referred to as
"post pipeline sanity checks". These types of checks go further than the "successful 
completion" in that they examine contents and relationships between contents of 
files produced by the indicated type of processing. 

Another set of "checks" are simply written to collect data about the pipeline
processing. For example, CollectTopologyCorrectionNumbers is not checking for the 
successful completion of pipeline processing or performing a sanity check. Instead,
it is collecting data about how many topology corrections are done (an their size)
in the structural preprocessing.

* CheckForOtherSubjectsData

  - Special test written to check for condition in which one subject has 
    another subject's data files in it's resources

* CheckFunctionalPreprocessing

  - Post Pipeline Sanity Check for functional preprocessing

* CheckPackageExistence

  - Checks for the existence of Structural, Functional, and Diffusion 
    preprocessed packages for a project

* CollectTopologyCorrectionNumbers

  - Looks through the provenance archive for Structural_preproc resources
    containing log files named StructuralHCP.log.  Those logs are searched
    for lines indicating defect corrections.

* CompletionChecks

  - Main checks for pipeline completion. 
    - Old: <code>getPipelineResources</code>
    - New: <code>CheckHcpPipelineStatus</code>
   

<!-- References -->
[HCP]: http://www.humanconnectome.org
