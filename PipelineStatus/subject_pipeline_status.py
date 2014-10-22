import datetime

class SubjectPipelineStatus(object):

    def __init__(self, subject_id):
        super(SubjectPipelineStatus, self).__init__()
        self._subject_id = subject_id
        #self._submission_datetime = datetime.datetime()

    # property subject_id
    def _get_subject_id(self):
        return self._subject_id

    subject_id=property(_get_subject_id)

    def __str__(self):
        return "Pipeline status for subject: " + str(self.subject_id)


    


