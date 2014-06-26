Completion Checks
=================

# Description

CompletionChecks contains two Python scripts <code>getPipelineResources</code> and <code>CheckHcpPipelineStatus</code>.
<code>getPipelineResources</code> was originally written by Tony Wilson and was used before the 500 Subject 
Release to check on the completion status of [Human Connectome Project][HCP] Minimal Preprocessing Pipeline pipeline
processing.

<code>CheckHcpPipelineStatus</code> started out based on <code>getPipelineResources</code> to perform similar
checks for the processing leading up to the 500 Subject Release.  <code>CheckHcpPipelineStatus</code> is intended
to be easier to understand and modify than <code>getPipelineResources</code>.  Its purpose and flow _should_ be
more clear.

<!-- References -->
[HCP]: http://www.humanconnectome.org
