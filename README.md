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

<!-- References -->
[HCP]: http://www.humanconnectome.org
