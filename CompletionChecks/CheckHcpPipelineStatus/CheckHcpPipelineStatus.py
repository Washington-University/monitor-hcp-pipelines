"""CheckHcpPipelineStatus.py

   Check the status of pipelines run on HCP data
"""

# Global Data

# Indicator of whether to output debugging information
g_debug=False

class CommandLineOptions(object):
    """Class for storing command line options specified for this program"""
    def __init__(self, user_name, password, server_name, 
                 pipeline, project, subjects, output_path, verbose):
        """initialize an instance
        
        :param user_name: the XNAT user name 
        :type user_name: string
        :param password: the password for the XNAT user
        :type password: string
        :param server_name: the name of the XNAT server
        :type server_name: string
        :param pipeline: the classification of pipelines to check (structural, functional, diffusion)
        :type pipeline: string
        :param project: the XNAT project to check
        :type project: string
        :param subjects: the project subjects to check (comma separated list)
        :type subjects: string
        :param output_path: path to output file to produce
        :type output_path: string
        :param verbose: indication of whether verbose status information should be output to stdout
        :type verbose: boolean
        """
        super(CommandLineOptions, self).__init__()
        self.__user_name = user_name
        self.__password = password
        self.__server_name = server_name
        self.__pipeline = pipeline
        self.__project = project
        self.__subjects = subjects
        self.__output_path = output_path
        self.__verbose = verbose

    def get_user_name(self):
        """get the user name"""
        return self.__user_name

    def get_password(self):
        """get the password"""
        return self.__password

    def get_server_name(self):
        """get the XNAT server name"""
        return self.__server_name

    def get_pipeline(self):
        """get the pipeline classification indicator"""
        return self.__pipeline

    def get_project(self):
        """get the project"""
        return self.__project

    def get_subjects(self):
        """get the comma separated list of subjects"""
        return self.__subjects

    def get_output_path(self):
        """get the output file path"""
        return self.__output_path

    def get_verbose(self):
        """get the verbose indication"""
        return self.__verbose

class ProcessingStatus(object):
    """Class for keeping track of detected processing status"""
    def __init__(self, subject_id):
        """initialize an instance

        :param subject_id: id of the subject for the processing status
        :type subject_id: string
        """
        self.__subject_id = subject_id
        self.__resource_name = 'unknown'
        self.__resource_present = False
        self.__data_present = False

    def get_subject_id(self):
        """get the subject_id"""
        return self.__subject_id

    def set_resource_name(self, resource_name):
        """set the resource_name"""
        self.__resource_name = resource_name
    
    def get_resource_name(self):
        """get the resource_name"""
        return self.__resource_name

    def set_resource_present(self, resource_present):
        """set the indication of whether or not the resource is present"""
        self.__resource_present = resource_present
    
    def get_resource_present(self):
        """get the indication of whether or not the resource is present"""
        return self.__resource_present

    def set_data_present(self, data_present):
        """set the indication of whether or not the data is present"""
        self.__data_present = data_present
    
    def get_data_present(self):
        """get the indication of whether or not the data is present"""
        return self.__data_present

def vprint(verbose, input):
    """only print if in verbose mode"""
    if not verbose:
        return
    print str(input)

def parse_command_line():
    """parse the command line and return a CommandLineOptions object

    :return: CommandLineOptions object populated based on the specified command line options
    """
    import argparse
    import getpass

    parser = argparse.ArgumentParser(description="Check Pipeline Status")
    parser.add_argument("-vers", "--version", action="version", version="%(prog)s 0.2.0")
    parser.add_argument("-u", "--user", dest="user", required=True, help="User name", type=str)
    parser.add_argument("-p", "--password", dest="password", default="", help="Password", type=str)
    parser.add_argument("-s", "--server", dest="server", default="https://db.humanconnectome.org", help="DB Server", type=str)
    parser.add_argument("-pl", "--pipeline", dest="pipeline", required=True, help="Pipeline [structural|functional|diffusion|fix|task]", type=str)
    parser.add_argument("-pr", "--project", dest="project", required=True, help="Project", type=str)
    parser.add_argument("-su", "--subjects", dest="subjects", default="All", 
                        help="Comma separated list of subjects. If not supplied check all subjects in project", type=str)
    parser.add_argument("-o", "--output", dest="output", default="CheckHcpPipelineStatus.output.txt", type=str)
    parser.add_argument("-verb", "--verbose", dest="verbose", default=False, type=bool)

    args = parser.parse_args()

    if (args.password == ""):
        args.password = getpass.getpass()

    command_line_options = CommandLineOptions(
        args.user, args.password, args.server, args.pipeline, args.project, args.subjects, args.output, args.verbose)

    return command_line_options

def show_options(command_line_options):
    """output to stdout the retrieved command line option values

    :param command_line_options: the populated command line options object to show

    Only outputs values if g_debug is True.
    """
    if not g_debug:
        return

    print "User Name: " + str(command_line_options.get_user_name())
    print "Password : " + "************"
    print "Server   : " + str(command_line_options.get_server_name())
    print "Pipeline : " + str(command_line_options.get_pipeline())
    print "Project  : " + str(command_line_options.get_project())
    print "Subjects : " + str(command_line_options.get_subjects())
    print "Output   : " + str(command_line_options.get_output_path())
    print "Verbose  : " + str(command_line_options.get_verbose())

def output_processing_status(outfile, status):
    """output processing status information to the specified file
    
    :param outfile: the output file to which to write
    :type outfile: file object
    :param status: the status information to write
    :type status: ProcessingStatus
    """
    outfile.write('\t'.join([status.get_subject_id(), status.get_resource_name(), 
                             str(status.get_resource_present()), str(status.get_data_present())]))
    outfile.write('\n')

def create_output_file(output_path, status_list):
    """create the output file containing processing status values

    :param output_path: path to output file
    :type output_path: string
    :param status_list: list of processing status objects
    :type status_list: list of ProcessingStatus objects
    """
    last_subject_id = ""

    HeaderStr = ['SubjectID', 'Resource', 'Resources Present', 'Data Present']
    with open(output_path, 'w') as output_file:
        output_file.write('\t'.join(HeaderStr))
        output_file.write('\n')
        for status in status_list:
            if (status.get_subject_id() != last_subject_id):
                output_file.write('\n')
                last_subject_id = status.get_subject_id()

            output_processing_status(output_file, status)

def check_structural_status(verbose, getHCP, subject_to_check):
    """check the status of structural processing for a subject
    
    :param verbose: indication of whether to include verbose processing status info on stdout
    :type verbose: bool
    :param getHCP: object to interact with HCP database
    :type getHCP: getHCP
    :param subject_to_check: indication of which subject to check
    :type subject_to_check: string
    :return ProcessingStatus: indication of processing status for checked subject
    """

    vprint(verbose, "\nChecking structual preprocessing status for subject: " + subject_to_check)

    # List of names of files to look for on structural preprocessing resource
    structural_file_names = [
        'T1w_acpc_dc_restore_brain.nii.gz',
        'T1w_acpc_dc_restore.nii.gz', 
        'T1w_acpc_dc.nii.gz', 
        'T1wDividedByT2w_ribbon.nii.gz', 
        'T1wDividedByT2w.nii.gz', 
        'T2w_acpc_dc_restore_brain.nii.gz',
        'T2w_acpc_dc_restore.nii.gz', 
        'T2w_acpc_dc.nii.gz', 
        'aparc.a2009s+aseg.nii.gz', 
        'aparc+aseg.nii.gz']

    resource_name = 'Structural_preproc'
    getHCP.Subject = subject_to_check
    getHCP.Session = "%s_3T" % getHCP.Subject
    processing_status = ProcessingStatus(getHCP.Subject)
    subjectResources = getHCP.getSubjectResources()

    if ('404 Error' in subjectResources):
        error_msg = "Subject %s not found." % getHCP.Subject
        print error_msg
        processing_status.set_resource_name(error_msg)
        processing_status.set_resource_present(False)
        processing_status.set_data_present(False)

    else:
        subjectResourceNames = subjectResources.get('Names')
        processing_status.set_resource_name(resource_name)

        vprint(verbose, "\n\tChecking for presence of resource: " + resource_name)

        if (resource_name in subjectResourceNames):
            vprint(verbose, "\tResource " + resource_name + " present")
            processing_status.set_resource_present(True)

            data_count = 0
            getHCP.Resource = resource_name
            preprocMeta = getHCP.getSubjectResourceMeta()

            for k in xrange(0, len(structural_file_names)):
                vprint(verbose, "\tChecking for presence of file: " + structural_file_names[k])
                if (structural_file_names[k] in preprocMeta.get('Name')):
                    vprint(verbose, "\tFile: " + structural_file_names[k] + " present")
                    data_count += 1
                else:
                    vprint(verbose, "\tFile: " + structural_file_names[k] + " not present")

            if (data_count == len(structural_file_names)):
                vprint(verbose, "\tAll checked files present")
                processing_status.set_data_present(True)
            else:
                vprint(verbose, "\tSome checked files not present")
                processing_status.set_data_present(False)

        else:
            vprint(verbose, "\tResource " + resource_name + " not present")
            processing_status.set_resource_present(False)
            processing_status.set_data_present(False)

    return processing_status


def check_diffusion_status(verbose, getHCP, subject_to_check):
    """check the status of diffusion processing for a subject
    
    :param verbose: indication of whether to include verbose processing status info on stdout
    :type verbose: bool
    :param getHCP: object to interact with HCP database
    :type getHCP: getHCP
    :param subject_to_check: indication of which subject to check
    :type subject_to_check: string
    :return ProcessingStatus: indication of processing status for checked subject
    """

    vprint(verbose, "\nChecking diffusion preprocessing status for subject: " + subject_to_check)

    # List of names of files to look for on diffusion preprocessing resource
    diffusion_file_names = [
        'T1w_acpc_dc_restore_1mm.nii.gz',   # This file exists before diffusion preprocessing is done
        'T1w_acpc_dc_restore_1.25.nii.gz',  # This file does not exist before diffusion preprocessing is done, and doesn't exist after the pre-eddy phase either.
        'bvals',                            # This file does not exist before diffusion preprocessing is done, and doesn't exist after the pre-eddy phase either.
        'bvecs',                            # This file does not exist before diffusion preprocessing is done, and doesn't exist after the pre-eddy phase either.
        'data.nii.gz',                      # This file does not exist before diffusion preprocessing is done, and doesn't exist after the pre-eddy phase either.
        'nodif_brain_mask.nii.gz',          # This file is created by the pre-eddy phase.
        'grad_dev.nii.gz']                  # This file does not exist before diffusion preprocessing is done, and doesn't exist after the pre-eddy phase either.


    # Other potential files to check
    # 
    # The following files are created by the Pre-Eddy phase of Diffusion Preprocessing
    #
    #   Diffusion/data - directory
    #   
    #   Diffusion/eddy - directory
    #   Diffusion/eddy/series_index.txt
    #   Diffusion/eddy/index.txt
    #   Diffusion/eddy/acqparams.txt
    #   Diffusion/eddy/Pos_SeriesVolNum.txt
    #   Diffusion/eddy/Pos_Neg.nii.gz
    #   Diffusion/eddy/Pos_Neg.bvecs
    #   Diffusion/eddy/Pos_Neg.bvals
    #   Diffusion/eddy/Pos.bvec
    #   Diffusion/eddy/Pos.bval
    #   Diffusion/eddy/Neg_SeriesVolNum.txt
    #   Diffusion/eddy/Neg.bvec
    #   Diffusion/eddy/Neg.bval
    #   
    #   Diffusion/rawdata - directory
    #   Diffusion/rawdata/RL_SeriesCorrespVolNum.txt
    #   Diffusion/rawdata/RL_3.nii.gz
    #   Diffusion/rawdata/RL_3.bvec
    #   Diffusion/rawdata/RL_3.bval
    #   Diffusion/rawdata/RL_2.nii.gz
    #   Diffusion/rawdata/RL_2.bvec
    #   Diffusion/rawdata/RL_2.bval
    #   Diffusion/rawdata/RL_1.nii.gz
    #   Diffusion/rawdata/RL_1.bvec
    #   Diffusion/rawdata/RL_1.bval
    #   Diffusion/rawdata/LR_SeriesCorrespVolNum.txt
    #   Diffusion/rawdata/LR_3.nii.gz
    #   Diffusion/rawdata/LR_3.bvec
    #   Diffusion/rawdata/LR_3.bval
    #   Diffusion/rawdata/LR_2.nii.gz
    #   Diffusion/rawdata/LR_2.bvec
    #   Diffusion/rawdata/LR_2.bval
    #   Diffusion/rawdata/LR_1.nii.gz
    #   Diffusion/rawdata/LR_1.bvec
    #   Diffusion/rawdata/LR_1.bval
    #
    #   Diffusion/reg - directory
    #
    #   Diffusion/topup - directory
    #   Diffusion/topup/topup_Pos_Neg_b0_movpar.txt
    #   Diffusion/topup/topup_Pos_Neg_b0_fieldcoef.nii.gz
    #   Diffusion/topup/nodif_brain_mask.nii.gz
    #   Diffusion/topup/nodif_brain.nii.gz
    #   Diffusion/topup/hifib0.nii.gz
    #   Diffusion/topup/extractedb0.txt
    #   Diffusion/topup/acqparams.txt
    #   Diffusion/topup/Pos_Neg_b0.topup_log
    #   Diffusion/topup/Pos_Neg_b0.nii.gz
    #
    #   T1w/Diffusion - directory 

    resource_name = 'Diffusion_preproc'
    getHCP.Subject = subject_to_check
    getHCP.Session = "%s_3T" % getHCP.Subject
    processing_status = ProcessingStatus(getHCP.Subject)
    subjectResources = getHCP.getSubjectResources()

    if ('404 Error' in subjectResources):
        error_msg = "Subject %s not found." % getHCP.Subject
        print error_msg
        processing_status.set_resource_name(error_msg)
        processing_status.set_resource_present(False)
        processing_status.set_data_present(False)
 
    else:
       subjectResourceNames = subjectResources.get('Names')
       processing_status.set_resource_name(resource_name)

       vprint(verbose, "\n\tChecking for presence of resource: " + resource_name)

       if (resource_name in subjectResourceNames):
           vprint(verbose, "\tResource " + resource_name + " present")
           processing_status.set_resource_present(True)

           data_count = 0
           getHCP.Resource = resource_name
           preprocMeta = getHCP.getSubjectResourceMeta()
           
           for k in xrange(0, len(diffusion_file_names)):
               vprint(verbose, "\tChecking for presence of file: " + diffusion_file_names[k])
               if (diffusion_file_names[k] in preprocMeta.get('Name')):
                   vprint(verbose, "\tFile: " + diffusion_file_names[k] + " present")
                   data_count += 1
               else:
                   vprint(verbose, "\tFile: " + diffusion_file_names[k] + " not present")
                   
           if (data_count == len(diffusion_file_names)):
               vprint(verbose, "\tAll checked files present")
               processing_status.set_data_present(True)
           else:
               vprint(verbose, "\tSome checked files not present")
               processing_status.set_data_present(False)

       else:
           vprint(verbose, "\tResource " + resource_name + " not present")
           processing_status.set_resource_present(False)
           processing_status.set_data_present(False)

    return processing_status
    
def check_functional_status(verbose, getHCP, subject_to_check):
    """check the status of functional processing for a subject

    :param getHCP: object to interact with HCP database
    :type getHCP: getHCP
    :param subject_to_check: indication of which subject to check
    :type subject_to_check: string
    :return ProcessingStatusList: list of indications of processing status for checked subject
    """
    vprint(verbose, "\nChecking functional preprocessing status for subject: " + subject_to_check)

    functional_task_names = [
        'rfMRI_REST1',
        'rfMRI_REST2',
        'tfMRI_WM',
        'tfMRI_GAMBLING',
        'tfMRI_MOTOR',
        'tfMRI_LANGUAGE',
        'tfMRI_RELATIONAL',
        'tfMRI_SOCIAL',
        'tfMRI_EMOTION']
    
    # List of names of files to look for on functional preprocessing resource
    functional_file_names = [
        'Movement_Regressors_dt.txt', 
        'Movement_Regressors.txt', 
        'goodvoxels.nii.gz']

    # Build list of resources to check
    functional_task_list = list()
    unproc_task_list = list()
    for i in xrange(0, len(functional_task_names)):
        functional_task_list.append(functional_task_names[i]+"_RL_preproc")
        unproc_task_list.append(functional_task_names[i]+"_RL_unproc")
        functional_task_list.append(functional_task_names[i]+"_LR_preproc")
        unproc_task_list.append(functional_task_names[i]+"_LR_unproc")

    functional_processing_status_list = list()

    getHCP.Subject = subject_to_check
    getHCP.Session = "%s_3T" % getHCP.Subject
    subjectResources = getHCP.getSubjectResources()

    if ('404 Error' in subjectResources):
        error_msg = "Subject %s not found." % getHCP.Subject
        print error_msg
        functional_processing_status = ProcessingStatus(getHCP.Subject)
        functional_processing_status.set_resource_name(error_msg)
        functional_processing_status.set_resource_present(False)
        functional_processing_status.set_data_present(False)

        functional_processing_status_list.append(functional_processing_status)

    else:
        subjectResourceNames = subjectResources.get('Names')

        for i in xrange(0, len(functional_task_list)):
            vprint(verbose, "\n\tDetermining if resource: " + functional_task_list[i] + " should be present")

            if (unproc_task_list[i] not in subjectResourceNames):
                vprint(verbose, "\tNo need to check for resource: " + functional_task_list[i] + " because " + unproc_task_list[i] + " is not present")
                functional_processing_status = ProcessingStatus(getHCP.Subject)
                functional_processing_status.set_resource_name(functional_task_list[i] + " unproc not present")
                functional_processing_status.set_resource_present(False)
                functional_processing_status.set_data_present(False)
                functional_processing_status_list.append(functional_processing_status)

            else:
                vprint(verbose, "\n\tChecking for presence of resource: " + functional_task_list[i])
                functional_processing_status = ProcessingStatus(getHCP.Subject)
                functional_processing_status.set_resource_name(functional_task_list[i])
            
                if (functional_task_list[i] not in subjectResourceNames):
                    vprint(verbose, "\tResource " + functional_task_list[i] + " not present")
                    functional_processing_status.set_resource_present(False)
                    functional_processing_status.set_data_present(False)
                else:
                    vprint(verbose, "\tResource " + functional_task_list[i] + " present")
                    functional_processing_status.set_resource_present(True)

                    getHCP.Resource = functional_task_list[i]
                    preprocMeta = getHCP.getSubjectResourceMeta()

                    if (preprocMeta != 500):
                        data_count = 0
                        for k in xrange(0, len(functional_file_names)):
                            vprint(verbose, "\tChecking for presence of file: " + functional_file_names[k])
                            if (functional_file_names[k] in preprocMeta.get('Name')):
                                vprint(verbose, "\tFile: " + functional_file_names[k] + " present")
                                data_count += 1
                            else:
                                vprint(verbose, "\tFile: " + functional_file_names[k] + " not present")
                                
                        if (data_count == len(functional_file_names)):
                            vprint(verbose, "\tAll checked files present")
                            functional_processing_status.set_data_present(True)
                        else:
                            vprint(verbose, "\tSome checked files not present")
                            functional_processing_status.set_data_present(False)
                    else:
                        functional_processing_status.set_data_present(False)

                functional_processing_status_list.append(functional_processing_status)

    return functional_processing_status_list

def check_fix_status(verbose, getHCP, subject_to_check):
    """check the status of ica-fix processing for a subject

    :param verbose: indication of whether to include verbose processing status info on stdout
    :type verbose: bool
    :param getHCP: object to interact with HCP database
    :type getHCP: getHCP
    :param subject_to_check: indication of which subject to check
    :type subject_to_check: string
    :return ProcessingStatusList: list of indications of processing status for checked subject
    """
    
    vprint(verbose, "\nChecking ICA+FIX status for subject: " + subject_to_check)

    fix_task_names = [
        'rfMRI_REST1',
        'rfMRI_REST2']

    # List of names of files to look for in fix resource
    fix_file_names = [
        'fix4melview_HCP_hp2000_thr10.txt', 
        'eigenvalues_percent', 
        'melodic_FTmix', 
        'melodic_IC.nii.gz', 
        'melodic_ICstats', 
        'melodic_mix', 
        'melodic_oIC.nii.gz', 
        'melodic_Tmodes']

    # List of file name suffixes to look for in fix resource
    fix_suffix_list = [
        '_hp2000_clean.nii.gz',
        '_Atlas_hp2000_clean.dtseries.nii', 
        '_hp2000.nii.gz']

    # Build list of resources to check
#    fix_task_list = list()
#    preproc_task_list = list()
#    for i in xrange(0, len(fix_task_names)):
#        fix_task_list.append(fix_task_names[i]+"_RL_FIX")
#        preproc_task_list.append(fix_task_names[i]+"_RL_preproc")
#        fix_task_list.append(fix_task_names[i]+"_LR_FIX")
#        preproc_task_list.append(fix_task_names[i]+"_LR_preproc")

    fix_task_list = list()
    for i in xrange(0, len(fix_task_names)):
        fix_task_list.append(fix_task_names[i]+"_RL")
        fix_task_list.append(fix_task_names[i]+"_LR")

    fix_resource_list = list()
    preproc_resource_list = list()
    for i in xrange(0, len(fix_task_list)):
        fix_resource_list.append(fix_task_list[i]+"_FIX")
        preproc_resource_list.append(fix_task_list[i]+"_preproc")


    fix_processing_status_list = list()
        
    getHCP.Subject = subject_to_check
    getHCP.Session = "%s_3T" % getHCP.Subject
    subjectResources = getHCP.getSubjectResources()

    if ('404 Error' in subjectResources):
        error_msg = "Subject %s not found." % getHCP.Subject
        print error_msg
        fix_processing_status = ProcessingStatus(getHCP.Subject)
        fix_processing_status.set_resource_name(error_msg)
        fix_processing_status.set_resource_present(False)
        fix_processing_status.set_data_present(False)

        fix_processing_status_list.append(fix_processing_status)

    else:
        subjectResourceNames = subjectResources.get('Names')

        for i in xrange(0, len(fix_resource_list)):
            vprint(verbose, "\n\tDetermining if resource: " + fix_resource_list[i] + " should be present")

            if (preproc_resource_list[i] not in subjectResourceNames):
                vprint(verbose, "\tNo need to check for resource: " + fix_resource_list[i] + " because " + preproc_resource_list[i] + " is not present")
                fix_processing_status = ProcessingStatus(getHCP.Subject)
                fix_processing_status.set_resource_name(fix_resource_list[i] + " preproc not present")
                fix_processing_status.set_resource_present(False)
                fix_processing_status.set_data_present(False)
                fix_processing_status_list.append(fix_processing_status)

            else:
                vprint(verbose, "\n\tChecking for presence of resource: " + fix_resource_list[i])
                fix_processing_status = ProcessingStatus(getHCP.Subject)
                fix_processing_status.set_resource_name(fix_resource_list[i])

                if (fix_resource_list[i] not in subjectResourceNames):
                    vprint(verbose, "\tResource: " + fix_resource_list[i] + " not present")
                    fix_processing_status.set_resource_present(False)
                    fix_processing_status.set_data_present(False)
                else:
                    vprint(verbose, "\tResource: " + fix_resource_list[i] + " present")
                    fix_processing_status.set_resource_present(True)

                    getHCP.Resource = fix_resource_list[i]
                    preprocMeta = getHCP.getSubjectResourceMeta()

                    if (preprocMeta != 500):
                        data_count = 0
                        for k in xrange(0, len(fix_file_names)):
                            vprint(verbose, "\tChecking for presence of file: " + fix_file_names[k])
                            if (fix_file_names[k] in preprocMeta.get('Name')):
                                vprint(verbose, "\tFile: " + fix_file_names[k] + " present")
                                data_count += 1
                            else:
                                vprint(verbose, "\tFile: " + fix_file_names[k] + " not present")

                        for k in xrange(0, len(fix_suffix_list)):
                            file_to_check = fix_task_list[i] + fix_suffix_list[k]
                            vprint(verbose, "\tChecking for presence of file: " + file_to_check)
                            if (file_to_check in preprocMeta.get('Name')):
                                vprint(verbose, "\tFile: " + file_to_check + " present")
                                data_count += 1
                            else:
                                vprint(verbose, "\tFile: " + file_to_check + " not present")

                        if (data_count == len(fix_file_names) + len(fix_suffix_list)):
                            vprint(verbose, "\tAll checked files present")
                            fix_processing_status.set_data_present(True)
                        else:
                            vprint(verbose, "\tSome checked files not present")
                            fix_processing_status.set_data_present(False)
                        
                    else:
                        fix_processing_status.set_data_present(False)

                fix_processing_status_list.append(fix_processing_status)

    return fix_processing_status_list

def check_task_analysis_status(verbose, getHCP, subject_to_check):

    vprint(verbose, "\nChecking task analysis status for subject: " + subject_to_check)

    task_names = [
        'tfMRI_WM',
        'tfMRI_GAMBLING',
        'tfMRI_MOTOR',
        'tfMRI_LANGUAGE',
        'tfMRI_RELATIONAL',
        'tfMRI_SOCIAL',
        'tfMRI_EMOTION']

    # List of names of files to look for on task analysis resource
    task_file_names = [
        'Contrasts.txt',
        'weights1.nii.gz',
        'fstat1.dtseries.nii']

    task_file_name_expected_counts = [
        4, 
        6,
        8]

    # Build list of resources to check
    task_list = list()
    for i in xrange(0, len(task_names)):
        task_list.append(task_names[i])

    task_analysis_processing_status_list = list()

    getHCP.Subject = subject_to_check
    getHCP.Session = "%s_3T" % getHCP.Subject
    subjectResources = getHCP.getSubjectResources()

    if ('404 Error' in subjectResources):
        error_msg = "Subject %s not found." % getHCP.Subject
        print error_msg
        task_analysis_processing_status = ProcessingStatus(getHCP.Subject)
        task_analysis_processing_status.set_resource_name(error_msg)
        task_analysis_processing_status.set_resource_present(False)
        task_analysis_processing_status.set_data_present(False)

        task_analysis_processing_status_list.append(task_analysis_processing_status)

    else:
        subjectResourceNames = subjectResources.get('Names')

        for i in xrange(0, len(task_list)):
            vprint(verbose, "\n\tChecking for presence of resource: " + task_list[i])
            task_analysis_processing_status = ProcessingStatus(getHCP.Subject)
            task_analysis_processing_status.set_resource_name(task_list[i])

            if (task_list[i] not in subjectResourceNames):
                vprint(verbose, "\tResource " + task_list[i] + " not present")
                task_analysis_processing_status.set_resource_present(False)
                task_analysis_processing_status.set_data_present(False)
            else:
                vprint(verbose, "\tResource " + task_list[i] + " present")
                task_analysis_processing_status.set_resource_present(True)

                getHCP.Resource = task_list[i]
                resourceMeta = getHCP.getSubjectResourceMeta()

                if (resourceMeta != 500):
                    data_count = 0
                    for k in xrange(0, len(task_file_names)):
                        vprint(verbose, "\tChecking for at least " + str(task_file_name_expected_counts[k]) + " files named: " + task_file_names[k])

                        count = resourceMeta.get('Name').count(task_file_names[k])
                        vprint(verbose, "\tFound " + str(count) + " files named: " + task_file_names[k])
                        if (count >= task_file_name_expected_counts[k]):
                            vprint(verbose, "\tFile: " + task_file_names[k] + " expected number present")
                            data_count += 1
                        else:
                            vprint(verbose, "\tFile: " + task_file_names[k] + " expected number not present")

                    if (data_count == len(task_file_names)):
                        vprint(verbose, "\tAll checked files present")
                        task_analysis_processing_status.set_data_present(True)
                    else:
                        vprint(verbose, "\tSome checked files not present")
                        task_analysis_processing_status.set_data_present(False)
                else:
                    task_analysis_processing_status.set_data_present(False)

            task_analysis_processing_status_list.append(task_analysis_processing_status)

    return task_analysis_processing_status_list


def main():
    """main function of this Python program"""
    from pyHCP import pyHCP, getHCP

    command_line_options = parse_command_line()
    show_options(command_line_options)

    Username   = command_line_options.get_user_name()
    Password   = command_line_options.get_password()
    Server     = command_line_options.get_server_name()
    Pipeline   = command_line_options.get_pipeline()
    Project    = command_line_options.get_project()
    Subjects   = command_line_options.get_subjects()
    OutputPath = command_line_options.get_output_path()
    Verbose    = command_line_options.get_verbose()

    pyHCP = pyHCP(Username, Password, Server)
    getHCP = getHCP(pyHCP)
    getHCP.Project = Project

    if (Subjects is not "All"):
        subjects_to_check = ((Subjects.split(',')))
    else:
        subjects_to_check = getHCP.getSubjects()

    processing_status_list = list()

    # Cycle through specified subjects to check
    for i in xrange(0, len(subjects_to_check)):
        if ('struct' in Pipeline.lower()):
            structural_processing_status = check_structural_status(Verbose, getHCP, subjects_to_check[i])
            processing_status_list.append(structural_processing_status)

        if ('funct' in Pipeline.lower()):
            functional_processing_status_list = check_functional_status(Verbose, getHCP, subjects_to_check[i])
            for functional_processing_status in functional_processing_status_list:
                processing_status_list.append(functional_processing_status)

        if ('diff' in Pipeline.lower()):
            diffusion_processing_status = check_diffusion_status(Verbose, getHCP, subjects_to_check[i])
            processing_status_list.append(diffusion_processing_status)

        if ('fix' in Pipeline.lower()):
            fix_processing_status_list = check_fix_status(Verbose, getHCP, subjects_to_check[i])
            for fix_processing_status in fix_processing_status_list:
                processing_status_list.append(fix_processing_status)

        if ('task' in Pipeline.lower()):
            task_processing_status_list = check_task_analysis_status(Verbose, getHCP, subjects_to_check[i])
            for task_processing_status in task_processing_status_list:
                processing_status_list.append(task_processing_status)

    # Output Results
    create_output_file(OutputPath, processing_status_list)
            
#
# Invoke main to get things started
#
import time

startTime = time.time()
main()
duration = time.time() - startTime
print("Duration: %s seconds" % duration)






