# Usage Notes for checking on the status of HCP pipeline processing

## WUSTL Center for High Performance Computing access

For the [Human Connectome Project][HCP] (HCP) 500 Subject Release, the Minimal Preprocessing Pipelines (MPP) were 
run on the WUSTL Center for High Performance Computing (CHPC) cluster.  To access the CHPC system via a login node
from an NRG login in order to check on the status of jobs, do the following:

<pre>
        [yourloginid@hcpx-dev-you1 ~]$ sudo su - hcpexternal
        [hcpexternal@hcpx-dev-you1 ~]$ ssh -i ~/.ssh/chpc01_id_rsa HCPpipeline@login1.chpc.wustl.edu
        [HCPpipeline@login001 ~]$
</pre>

## Build directory and XNAT pipeline logs

The logs and output from running jobs are in a build directory on the CHPC machines.

<code>cd /HCP/hcpdb/build_ssd/chpc/BUILD</code> (or, as of this writing, <code>cd $BUILD\_DIR</code>)

Per subject/session build subdirectories will exist for jobs. They will be of the form <unix-timestamp>\_<subject-id>

In those subject-and-time-specific directories you will find and MPP directory containing the stdout for the MPP job (MPP.log) 
and the stderr for the MPP job (MPP.err). 

A log of jobs submitted to the queue for the subsequent parts of the pipeline (Structural, Functional, etc.) is
in a file named queue.log, which will contain the PBS job ids.

Scripts that were submitted will take the form <subject-id>\_<job-type>.sh

Keep in mind that the MPP pipeline actually consists of just submitting the jobs to the queue.  So the MPP
pipeline can be "done" pretty quickly (submit your jobs and end.)

The other types of processing will create their own build directories in the subject-and-time-specific build 
directories (e.g. STRUCTURAL) generally with data directories named by <subject-id> and logs in a logs directory.

## Job Dependencies

Structural Preprocessing consists of 2 PBS jobs, one that does the actual preprocessing and one that does 
the PUT of the data. (The PUT is the action of using an HTTP PUT to upload the created data back into the 
HCP database.)

Functional and Diffusion Preprocessing depend upon Structural Preprocessing being completed.  But are independent
of one another.  

For each functional task (<code>tfMRI\_WM\_LR, tfMRI\_WM\_RL, tfMRI\_EMOTION\_LR, tfMRI\_EMOTION\_RL, tfMRI\_RELATIONAL\_LR,
tfMRI\_RELATIONAL\_RL, rfMRI\_REST1\_LR, rfMRI\_REST1\_LR, </code> etc.) a functional preprocessing job and a dependent PUT job is created.

For each pair of directions, a packaging job is created that depends upon successful completion of the LR\_put and the RL\_put
jobs.

Diffusion Preprocessing is broken into 4 sequential jobs: pre\_eddy, eddy, post\_eddy, and diffusion\_put.
This is so that the eddy job can be submitted to a node/queue with access to a GPU.

There are:
* 2 structural preprocessing jobs
* 45 functional preprocessing jobs
  - 9 functional conditions (7 tasks and 2 resting states)
  - times 2 directions each (LR and RL)
  - equals 18 functional processing jobs 
  - add the 18 corresponding functional put jobs (36 jobs so far)
  - add the 9 functional packaging jobs (45 jobs)
* 4 diffusion jobs
* equals 51 jobs per subject not including the ICA FIX or fMRI Task Analysis

## PBS Job Status Commands

* All jobs submitted by HCPpipeline user: <code>$ qstat -u HCPpipeline</code>
* All jobs for _subj-id_ submitted by HCPpipeline user: <code>$ qstat -u HCPpipeline | grep _subj-id_</code>
* Check details on a specific job: <code>checkjob _job-id_</code>
* Peek at the PBS job stdout for a running job: <code>qpeek -o _job-id_</code>
  - Note: Normally the log files are "written" to their intended location until the job is complete.
* Peek at the PBS job stderr for a running job: <code>qpeek -e _job-id_</code>

## PBS Logs

The PBS (queuing system) log files are log files for the jobs themselves not for the script submitted to the job.
These files will contain information about the resources used (memory, time, etc.) and other diagnostic information
about the jobs.

The PBS stdout and stderr files are in: <code>/HCP/hcpdb/build\_hds/chpc/logs\_mpp/pbs</code> (as of this writing this directory 
is defined in the environment variable LOG\_DIR).

The location of these log files is determined by the <code># PBS</code> entries in the config files in:
<code>HCPpipeline@login001/pipeline/catalog/MPP/resources/config/CHPC</code>

There are some check\_resourceusage*.sh scripts which grab stuff out of thes PBS stdout and stderr files 
to generate summary CSV files.

<!-- References -->
[HCP]: http://www.humanconnectome.org
