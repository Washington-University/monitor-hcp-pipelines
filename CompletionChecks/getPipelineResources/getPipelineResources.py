'''
Created on 2012-12-11

@author: jwilso01
'''
# for reasonable sorting...
#import numpy
from collections import OrderedDict
# multiplatform stuff...
import os
import sys
import argparse
# Time manipulation...
import time
from datetime import datetime
# XML parsing...
#import xml.etr

from pyHCP import pyHCP, getHCP

sTime = time.time()

#===============================================================================
# -U tony -P passfoo -WS https://db.humanconnectome.org -Prj HCP_Q3 -D C:\tmp -F FIX_Q3.txt -PPL FIX -S 100408
# -U tony -P passfoo -WS http://db.humanconnectome.org:8080 -Prj HCP_Q2 -D C:\tmp\misc -F foo_task.txt -S 100307 -T true
# -U tony -P passfoo -WS http://db.humanconnectome.org:8080 -Prj HCP_Q3 -D C:\tmp -F Foo_Q3.txt -PPL fix -S 100408,366446,131924
#===============================================================================

#===============================================================================
# PARSE INPUT
#===============================================================================
parser = argparse.ArgumentParser(description="Program to figure out pipelines status via WORKFLOW XML...")
# input...
parser.add_argument("-U", "--User", dest="User", default='tony', type=str)
parser.add_argument("-P", "--Password", dest="Password", type=str)
parser.add_argument("-S", "--Subjects", dest="Subjects", default=None, help="pick subject, or a list of subjects")
parser.add_argument("-Prj", "--Project", dest="Project", type=str, default="HCP_Q3", help="pick project")
parser.add_argument("-WS", "--Server", dest="WebServer", type=str, default="https://intradb.humanconnectome.org", help="pick server")
parser.add_argument("-PPL", "--Pipeline", dest="Pipeline", type=str, help="Pipeline to check...")
# output...
parser.add_argument("-D", "--OutputDir", dest="OutputDir", type=str, help="output dir")
parser.add_argument("-F", "--OutputFile", dest="OutputFile", type=str, help="output file name")
parser.add_argument("-DF", "--OutputDirFile", dest="OutputDirFile", type=str, help="output dir and filename")
# timeout...
parser.add_argument("-t", "--time_out", dest="Timeout", type=float, default=256.0, help="change timeout")
# version...
parser.add_argument('--version', action='version', version='%(prog)s 0.9.3')

args = parser.parse_args()
User = args.User
Password = args.Password
Subjects = args.Subjects
Server = args.WebServer
Project = args.Project
Pipeline = args.Pipeline
OutputDir = args.OutputDir
OutputFile = args.OutputFile
OutputDirFile = args.OutputDirFile
#===============================================================================
# CHECK SOME INPUTS
#===============================================================================
if (OutputDir is not None):
    if (OutputDir[-1] != os.sep):
        OutputDir = os.path.normpath(OutputDir) + os.sep
else:
    print 'ERROR: Output directory not specified.'
    sys.exit()
    
if (OutputDirFile is not None):
    OutputDirFile = os.path.normpath(args.OutputDirFile)
elif (OutputDir is None) and (OutputDirFile is None):
    print 'ERROR: No output directory location specified.'
    sys.exit()
#===============================================================================
# GLOBALS
#===============================================================================
Print = True
TimeoutStep = 8.0
TimeoutMax = 1024.0
Timeout = args.Timeout
TimeoutDefault = args.Timeout
#===============================================================================
# SET UP OUTPUT
#===============================================================================
if (OutputDir[-1] != os.sep):
    OutputDir = OutputDir + os.sep
    
if not os.path.exists(OutputDir):
    os.makedirs(OutputDir)
            
# headerStr = ['SubjectID', 'DataType', 'Pipeline', 'Status', 'PercentComplete', 'Session', 'TimeLaunch', 'TimeCompletion', 'TimeLaunchEpoch']

#===============================================================================
# pyHCP INTERFACE...
#===============================================================================
pyHCP = pyHCP(User, Password, Server)
getHCP = getHCP(pyHCP)
getHCP.Project = Project
getHCP.Timeout = Timeout
#===============================================================================
# Series and Resources Lists...
#===============================================================================
AllFunctionalSeries = ['rfMRI_REST1_RL', 'rfMRI_REST1_LR', 'rfMRI_REST2_RL', 'rfMRI_REST2_LR', \
             'tfMRI_WM_RL', 'tfMRI_WM_LR', 'tfMRI_GAMBLING_RL', 'tfMRI_GAMBLING_LR', 'tfMRI_MOTOR_RL', 'tfMRI_MOTOR_LR', \
             'tfMRI_LANGUAGE_RL', 'tfMRI_LANGUAGE_LR', 'tfMRI_SOCIAL_RL', 'tfMRI_SOCIAL_LR', 'tfMRI_RELATIONAL_LR', 'tfMRI_RELATIONAL_RL', 'tfMRI_EMOTION_RL', 'tfMRI_EMOTION_LR']
AllFunctionalResources = ['rfMRI_REST1_RL_preproc', 'rfMRI_REST1_LR_preproc', 'rfMRI_REST2_RL_preproc', 'rfMRI_REST2_LR_preproc', \
             'tfMRI_WM_RL_preproc', 'tfMRI_WM_LR_preproc', 'tfMRI_GAMBLING_RL_preproc', 'tfMRI_GAMBLING_LR_preproc', 'tfMRI_MOTOR_RL_preproc', 'tfMRI_MOTOR_LR_preproc', 'tfMRI_LANGUAGE_RL_preproc', 'tfMRI_LANGUAGE_LR_preproc', \
             'tfMRI_SOCIAL_RL_preproc', 'tfMRI_SOCIAL_LR_preproc', 'tfMRI_RELATIONAL_LR_preproc', 'tfMRI_RELATIONAL_RL_preproc', 'tfMRI_EMOTION_RL_preproc', 'tfMRI_EMOTION_LR_preproc']
AllTaskResources = ['tfMRI_WM', 'tfMRI_GAMBLING', 'tfMRI_MOTOR', 'tfMRI_LANGUAGE', 'tfMRI_SOCIAL', 'tfMRI_RELATIONAL', 'tfMRI_EMOTION']
AllFixResources = ['rfMRI_REST1_RL_FIX', 'rfMRI_REST1_LR_FIX', 'rfMRI_REST2_RL_FIX', 'rfMRI_REST2_LR_FIX']
#===============================================================================
# Resource File Names Lists...
#===============================================================================
AllStatus = ['Failed', 'Complete', 'Running']
StructuralNames = ['T1w_acpc_dc_restore_brain.nii.gz', 'T1w_acpc_dc_restore.nii.gz', 'T1w_acpc_dc.nii.gz', 'T1wDividedByT2w_ribbon.nii.gz', 'T1wDividedByT2w.nii.gz', 'T2w_acpc_dc_restore_brain.nii.gz', \
                 'T2w_acpc_dc_restore.nii.gz', 'T2w_acpc_dc.nii.gz', 'aparc.a2009s+aseg.nii.gz', 'aparc+aseg.nii.gz']
#FunctionalTail = ['_Atlas.dtseries.nii', '_Jacobian.nii.gz', '_SBRef.nii.gz', '.nii.gz']
#FunctionalNames = ['Movement_Regressors_dt.txt', 'Movement_Regressors.txt', 'goodvoxels.nii.gz', 'Movement_RelativeRMS.txt', 'Movement_RelativeRMS_mean.txt', 'Movement_AbsoluteRMS.txt', 'Movement_AbsoluteRMS_mean.txt']
FunctionalNames = ['Movement_Regressors_dt.txt', 'Movement_Regressors.txt', 'goodvoxels.nii.gz']
TaskLevel2Tail = ['_level2_hp200_s4.dscalar.nii', '_Atlas_hp200_s4.dtseries.nii', '_Atlas_hp200_s4.dtseries.nii']
TaskLevel2Names = ['Contrasts.txt', 'weights1.nii.gz', 'fstat1.dtseries.nii']

#FixNames = ['Atlas_hp_preclean.dtseries.nii']
#FixTails = ['_hp2000_clean.nii.gz', '_Atlas_hp2000_clean.dtseries.nii', '_hp2000.nii.gz']
FixNames = ['fix4melview_HCP_hp2000_thr5.txt', 'eigenvalues_percent', 'melodic_FTmix', 'melodic_IC.nii.gz', 'melodic_ICstats', 'melodic_mix', 'melodic_oIC.nii.gz', 'melodic_Tmodes']
FixTails = ['_hp2000_clean.nii.gz', '_Atlas_hp2000_clean.dtseries.nii', '_hp2000.nii.gz']

DiffNames = ['T1w_acpc_dc_restore_1mm.nii.gz', 'T1w_acpc_dc_restore_1.250.nii.gz', 'bvals', 'bvecs', 'data.nii.gz', 'nodif_brain_mask.nii.gz', 'grad_dev.nii.gz']
#===============================================================================

SubjectList = list()
SubjectResource = list()
if (Subjects is not None):
    Subjects = ((Subjects.split(',')))
else:
    Subjects = getHCP.getSubjects()
    
SuccessBool = list()
ResourceBool = list()
DataBool = list()

#Subjects = ['978578']
for i in xrange(0, len(Subjects)):
    print Subjects[i]
    print "Debug Point: A.1"
    getHCP.Subject = Subjects[i]
    print "Debug Point: A.2"
    getHCP.Session = '%s_3T' % getHCP.Subject
    print "Debug Point: A.3"
    subjectResources = getHCP.getSubjectResources()
    print "Debug Point: A.4"

    subjectSessionMeta = getHCP.getSessionMeta()
    print "Debug Point: A.5"
    subjectSeries = subjectSessionMeta.get('Series')
    print "Debug Point: A.6"
    subjectType = subjectSessionMeta.get('Types')
    print "Debug Point: A.7"
    
    FunctionalList = list()
    for j in xrange(0, len(subjectSessionMeta.get('Types'))):
        if ('fix' in Pipeline.lower()): # or ('task' in Pipeline.lower()):
            if (subjectSessionMeta.get('Types')[j] == 'rfMRI'):
                FunctionalList.append(subjectSessionMeta.get('Series')[j])
        elif ('struct' in Pipeline.lower()):
            if ('T1w' in subjectSessionMeta.get('Types')[j]) or ('T2w' in subjectSessionMeta.get('Types')[j]):
                FunctionalList.append(subjectSessionMeta.get('Series')[j])
        if ('funct' in Pipeline.lower()):
            if (subjectSessionMeta.get('Types')[j] == 'tfMRI') or (subjectSessionMeta.get('Types')[j] == 'rfMRI'):
                FunctionalList.append(subjectSessionMeta.get('Series')[j])
        elif ('task' in Pipeline.lower()):
            if (subjectSessionMeta.get('Types')[j] == 'tfMRI'):
#                    splitSeries = '_'.join(subjectSessionMeta.get('Series')[j].split('_')[0:2])
                FunctionalList.append('_'.join(subjectSessionMeta.get('Series')[j].split('_')[0:2]))

    print "Debug Point: B"

    if ('404 Error' in subjectResources):
        pass
    else:
        print "Debug Point: C"
        subjectResources = subjectResources.get('Names')
        SubjectListTmp = list()
        SubjectResourceTmp = list()
        SubjectResourceMissed = list()

        
        if ('task' in Pipeline.lower()):
            FunctionalList = list(set(FunctionalList))
            for j in xrange(0, len(FunctionalList)):
                if ('tfMRI' in FunctionalList[j]):
                    
                    if (FunctionalList[j]+'_LR_preproc' not in subjectResources) and (FunctionalList[j]+'_RL_preproc' not in subjectResources):
                        SubjectResource.append(FunctionalList[j])
                        SubjectList.append(getHCP.Subject)
                        DataBool.append(False)
                        ResourceBool.append(False)
                        
                    elif (FunctionalList[j]+'_LR_preproc' in subjectResources) and (FunctionalList[j]+'_RL_preproc' in subjectResources):
                        SubjectResource.append(FunctionalList[j])
                        SubjectList.append(getHCP.Subject)
                        ResourceBool.append(True)
            
                        getHCP.Resource = FunctionalList[j]
                        preprocMeta = getHCP.getSubjectResourceMeta()
                        
                        FilesBool = list()
                        if (preprocMeta != 500):
                            for k in xrange(0, len(TaskLevel2Names)):
                                if (TaskLevel2Names[k] in preprocMeta.get('Name')):
                                    FilesBool.append(True)
                                    
                            if (len(FilesBool) == (len(TaskLevel2Names))):
                                DataBool.append(True)
                            else:
                                DataBool.append(False)
                        else:
                            DataBool.append(500)
                    elif (FunctionalList[j]+'_LR_preproc' not in subjectResources) or (FunctionalList[j]+'_RL_preproc' not in subjectResources):
                        print 'Sheet, fell through with %s at function %s ' % (getHCP.Subject, FunctionalList[j])
                        SubjectResource.append(FunctionalList[j])
                        SubjectList.append(getHCP.Subject)
                        DataBool.append('NA')
                        ResourceBool.append('LR/RL')
                
        elif ('struct' in Pipeline.lower()):
            print "Debug Point: D"
#                    print subjectResources[j]
            if ('Structural_preproc' in subjectResources):
                ResourceBool.append(True)
                
                SubjectResource.append('Structural_preproc')
                SubjectList.append(getHCP.Subject)

                getHCP.Resource = 'Structural_preproc'
                preprocMeta = getHCP.getSubjectResourceMeta()
                
                DataCount = 0
                for k in xrange(0, len(StructuralNames)):
                    if (StructuralNames[k] in preprocMeta.get('Name')):
                        DataCount += 1

                if (DataCount == len(StructuralNames)):
                    DataBool.append(True)
                else:
                    DataBool.append(False)
            else:
                SubjectResource.append('Structural_preproc')
                SubjectList.append(getHCP.Subject)
                DataBool.append(False)
                ResourceBool.append(False)
                
        elif ('funct' in Pipeline.lower()):
            for j in xrange(0, len(FunctionalList)):
                if (('rfMRI' in FunctionalList[j]) or ('tfMRI' in FunctionalList[j])):
                    
                    rootSeries = '%s%s' % (FunctionalList[j], '_preproc')
                    
                    if (rootSeries not in subjectResources):
                        SubjectResource.append(rootSeries)
                        SubjectList.append(getHCP.Subject)
                        DataBool.append(False)
                        ResourceBool.append(False)
                        
                    elif (rootSeries in subjectResources):
                        SubjectResource.append(rootSeries)
                        SubjectList.append(getHCP.Subject)
                        ResourceBool.append(True)
            
                        getHCP.Resource = rootSeries
                        preprocMeta = getHCP.getSubjectResourceMeta()
                        
                        FilesBool = list()
                        if (preprocMeta != 500):
                            for k in xrange(0, len(FunctionalNames)):
                                if (FunctionalNames[k] in preprocMeta.get('Name')):
                                    FilesBool.append(True)
                                    
                            if (len(FilesBool) == (len(FunctionalNames))):
                                DataBool.append(True)
                            else:
                                DataBool.append(False)
                        else:
                            DataBool.append(500)
                            
        elif ('fix' in Pipeline.lower()):
            for j in xrange(0, len(FunctionalList)):
                if ('rfMRI' in FunctionalList[j]):
                    
                    rootSeries = '%s%s' % (FunctionalList[j], '_preproc')
                    fixSeries = '%s%s' % (FunctionalList[j], '_FIX')
                    print rootSeries, fixSeries
                    
#                        print rootSeries + '_FIX', rootSeries + '_preproc', subjectResources[j]
                    if (rootSeries in subjectResources) and (fixSeries in subjectResources):
                        print rootSeries + " and " + fixSeries + " present "
                        ResourceBool.append(True)
                        SubjectResource.append(FunctionalList[j])
                        SubjectList.append(getHCP.Subject)
                        
                        getHCP.Resource = fixSeries
                        preprocMeta = getHCP.getSubjectResourceMeta()
#                            print preprocMeta.get('Name')
                        
                        FilesBool = list()
                        for k in xrange(0, len(FixNames)):
                            print "Checking for presence of " + FixNames[k]
                            if (FixNames[k] in preprocMeta.get('Name')):
                                print "present"
#                                    print 'pyle!', FixNames[k]
                                FilesBool.append(True)
                            else:
                                print "Not present"
                                
                        for k in xrange(0, len(FixTails)):
                            print "Checking for presence of " + FunctionalList[j] + FixTails[k]
                            if (FunctionalList[j] + FixTails[k] in preprocMeta.get('Name')):
                                print "present"
#                                    print 'shazam!', rootSeries + FixTails[k]
                                FilesBool.append(True)
                            else:
                                print "Not present"
                                
                        if (len(FilesBool) == (len(FixNames) + len(FixTails))):
                            DataBool.append(True)
                        else:
                            DataBool.append(False)
                            
                    elif (rootSeries in subjectResources) and (fixSeries not in subjectResources):
                        SubjectResource.append(rootSeries + '_ALT')
                        SubjectList.append(getHCP.Subject)
                        ResourceBool.append(False)
                        DataBool.append(False)
                        
        elif ('diff' in Pipeline.lower()):
#                    print subjectResources[j]
            if ('Diffusion_preproc' in subjectResources):
                ResourceBool.append(True)
                
                SubjectResource.append('Diffusion_preproc')
                SubjectList.append(getHCP.Subject)

                getHCP.Resource = 'Diffusion_preproc'
                preprocMeta = getHCP.getSubjectResourceMeta()

                
                DataCount = 0
                for k in xrange(0, len(DiffNames)):
                    if (DiffNames[k] in preprocMeta.get('Name')):
                        DataCount += 1

                if (DataCount == len(DiffNames)):
                    DataBool.append(True)
                else:
                    DataBool.append(False)
            else:
                SubjectResource.append('Diffusion_preproc')
                SubjectList.append(getHCP.Subject)
                DataBool.append(False)
                ResourceBool.append(False)
                        
                
print len(SubjectList), len(SubjectResource), len(ResourceBool), len(DataBool)
if Print:
    # print len(subjectWorkflowSeriesAlt), len(subjectWorkflowStatusAlt), len(subjectTimeLaunchAlt), len(subjectTimeStepAlt), len(subjectTimeLaunchEpochAlt), len(subjectTimeStepEpochAlt)
    # HeaderStr = ['SubjectID', 'Series', 'Status', 'LaunchTime', 'CompletionTime', 'LaunchEpochTime', 'CompleteEpochTime']
    with open(OutputDir + OutputFile, 'wb') as OutputFileObj:
        HeaderStr = ['SubjectID', 'Resource', 'Resources Present', 'Data Present']
        OutputFileObj.write('\t'.join(HeaderStr))
        OutputFileObj.write('\n')
        for i in xrange(0, len(SubjectResource)):
            OutputFileObj.write('\t'.join([SubjectList[i], SubjectResource[i], str(ResourceBool[i]), str(DataBool[i])]))
            OutputFileObj.write('\n')
                    
    
print("Duration: %s" % (time.time() - sTime))

