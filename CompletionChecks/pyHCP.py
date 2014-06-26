'''
Created on 2012-12-19

@author: jwilso01
'''

# multiplatform system stuff...
import os
import sys
import errno
import hcp_constants
import subprocess
# Web stuff...
import socket
import urllib
import urllib2
import re
import time
#import requests
#import httplib2
from ssl import SSLError
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import QName
from urllib2 import URLError, HTTPError

#===============================================================================
# CLASSES
#===============================================================================
class pyHCP(object):
    """Main HCP Interfacing Class"""
    def __init__( self, User, Password, Server='intradb.humanconnectome.org' ):
        super(pyHCP, self).__init__()
        self.User = User
        self.Password = Password
        self.Server = self.cleanServer(Server)
        
    def cleanServer(self, Server):
        Server.strip()
        if (Server[-1] != '/'):
            Server = Server + '/'
        if (Server.find('http') == -1):
            Server = 'https://' + Server
        self.Server = Server
        return self.Server
    
    def getServer(self):
        return self.Server
        
class getHCP(pyHCP):
    """HCP Interfacing Class for GETs"""

    def __init__( self, pyHCP ):
        
        #=======================================================================
        # need to add a check for project existence.../
        #=======================================================================
        self.User = pyHCP.User
        self.Password = pyHCP.Password
        self.Server = pyHCP.Server
        
        self.Verbose = False
        self.Timeout = 8
        self.TimeoutMax = 1024
        self.TimeoutStep = 8
        
        self.Project = ''
        self.Projects = []
        self.ProjectNames = []
        self.ProjectsSecondary = []
        
        self.Session = ''
        self.Sessions = []
        self.SessionType = ''
        self.SessionTypes = []
        self.SessionParms = {}
        
        self.Subject = ''
        self.Subjects = []
        self.SubjectSessions = []
        self.SubjectSessionsUniq = []
        self.SubjectResourceMeta = {}
        self.SubjectResourcesMeta = {}
        
        self.AssessorDataType = ''
        
        self.Scan = ''
        self.Scans = []
        
        self.Resource = ''
        self.Resources = []
        
        self.FileInfo = {}
        self.ScanMeta = {}
        
        self.SessionId = self.getSessionId()
    #===============================================================================

    def getCurrentJSESSION(self):
        return self.SessionId
    #===============================================================================

    def getSessionId( self ):
        """Get session id for getHCP session spawn"""
        URL = self.Server + 'data/JSESSION'

        # URLLIB2
        Request = urllib2.Request(URL)
        basicPasswordManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        basicPasswordManager.add_password(None, URL, self.User, self.Password)
        basicAuthHandler = urllib2.HTTPBasicAuthHandler(basicPasswordManager)
        openerURL = urllib2.build_opener(basicAuthHandler)
        urllib2.install_opener(openerURL)

        while (self.Timeout <= self.TimeoutMax):
            try:
                connHandle = urllib2.urlopen(Request, None, self.Timeout)
                break
            except URLError, e:
                try:
                    code = e.code
                    if  (code != 401):
                        self.Timeout += self.TimeoutStep
                        print 'URLError code: ' +str(e.reason)+ '. Timeout increased to ' +str(self.Timeout)+' seconds for JSESSION cookie...'
                    else:
                        print 'URLError message: ' +str(e.msg)+ '. getSessionId Failed with wrong password.'
                        sys.exit(401)
                except:
                    try:
                        print 'URL: %s failed with code: %s ' % (URL, e.code)
                    except:
                        print 'URL: %s failed with reason: %s ' % (URL, e.reason)
                    sys.exit()
            except SSLError, e:
                self.Timeout += self.TimeoutStep
                print 'SSLError code: ' +str(e.message)+ '. Timeout increased to ' +str(self.Timeout)+' seconds for ' +URL
            except socket.timeout:
                self.Timeout += self.TimeoutStep
                print 'Socket timed out. Timeout increased to ' +str(self.Timeout)+ ' seconds for ' +URL
            
                
                
        self.SessionId = connHandle.read()
        return self.SessionId
    #===============================================================================
    def getURLString( self, URL ):
        """Get URL results as a string"""
        restRequest = urllib2.Request(URL)
        restRequest.add_header("Cookie", "JSESSIONID=" + self.SessionId);
    
        while (self.Timeout <= self.TimeoutMax):
            try:
                restConnHandle = urllib2.urlopen(restRequest, None, self.Timeout)
            except HTTPError, e:
                if (e.code == 400):
                    return '404 Error'
                elif (e.code == 500):
                    return '500 Error'
                elif (e.code != 404):
                    self.Timeout += self.TimeoutStep
                    print 'HTTPError code: ' +str(e.code)+ '. Timeout increased to ' +str(self.Timeout)+' seconds for ' +URL
                else:
                    print e
                    break
                    
            except URLError, e:
                self.Timeout += self.TimeoutStep
                print 'URLError code: ' +str(e.reason)+ '. Timeout increased to ' +str(self.Timeout)+' seconds for ' +URL
            except SSLError, e:
                self.Timeout += self.TimeoutStep
                print 'SSLError code: ' +str(e.message)+ '. Timeout increased to ' +str(self.Timeout)+' seconds for ' +URL
            except socket.timeout:
                self.Timeout += self.TimeoutStep
                print 'Socket timed out. Timeout increased to ' +str(self.Timeout)+ ' seconds for ' +URL
                
            else:
                try:
                    ReadResults = restConnHandle.read()
                    if ('"' in ReadResults) and ('xml' not in ReadResults):
                        return ReadResults.replace('"', '')
                    else:
                        return ReadResults
                    
                except HTTPError, e:
                    print 'READ HTTPError code: ' +str(e.code)+ '. File read timeout for ' +str(self.Timeout)+ ' seconds for ' +URL
                except URLError, e:
                    print 'READ URLError code: ' +str(e.reason)+ '. File read timeout for ' +str(self.Timeout)+' seconds for ' +URL
                except SSLError, e:
                    print 'READ SSLError code: ' +str(e.message)+ '. File read timeout for ' +str(self.Timeout)+' seconds for ' +URL
                except socket.timeout:
                    print 'READ Socket timed out. File read timeout for ' +str(self.Timeout)+ ' seconds for ' +URL
                    
        print 'ERROR: No reasonable timeout limit could be found for ' + URL
        sys.exit()
    #===============================================================================
    def getURLData( self, URL ):
        """Get URL results"""
        restRequest = urllib2.Request(URL)
        restRequest.add_header("Cookie", "JSESSIONID=" + self.SessionId);
    
        while (self.Timeout <= self.TimeoutMax):
            try:
                restConnHandle = urllib2.urlopen(restRequest, None, self.Timeout)
            except HTTPError, e:
                if (e.code == 400):
                    return '404 Error'
                elif (e.code == 500):
                    return '500 Error'
                elif (e.code != 404):
                    self.Timeout += self.TimeoutStep
                    print 'HTTPError code: ' +str(e.code)+ '. Timeout increased to ' +str(self.Timeout)+' seconds for ' +URL
                else:
                    print e
                    break
                    
            except URLError, e:
                self.Timeout += self.TimeoutStep
                print 'URLError code: ' +str(e.reason)+ '. Timeout increased to ' +str(self.Timeout)+' seconds for ' +URL
            except SSLError, e:
                self.Timeout += self.TimeoutStep
                print 'SSLError code: ' +str(e.message)+ '. Timeout increased to ' +str(self.Timeout)+' seconds for ' +URL
            except socket.timeout:
                self.Timeout += self.TimeoutStep
                print 'Socket timed out. Timeout increased to ' +str(self.Timeout)+ ' seconds for ' +URL
                
            else:
                try:
                    ReadResults = restConnHandle.read()
                    return ReadResults
                    
                except HTTPError, e:
                    print 'READ HTTPError code: ' +str(e.code)+ '. File read timeout for ' +str(self.Timeout)+ ' seconds for ' +URL
                except URLError, e:
                    print 'READ URLError code: ' +str(e.reason)+ '. File read timeout for ' +str(self.Timeout)+' seconds for ' +URL
                except SSLError, e:
                    print 'READ SSLError code: ' +str(e.message)+ '. File read timeout for ' +str(self.Timeout)+' seconds for ' +URL
                except socket.timeout:
                    print 'READ Socket timed out. File read timeout for ' +str(self.Timeout)+ ' seconds for ' +URL
                    
        print 'ERROR: No reasonable timeout limit could be found for ' + URL
        sys.exit()

    #===============================================================================
    def getProjects( self ):
        """Get a list of project names from XNAT instance"""
        
        restURL = self.Server + 'data/projects?format=csv'
        restResults = self.getURLString(restURL)
        
        restResultsSplit = restResults.split('\n')
        restEndCount = restResults.count('\n')
        restProjectHeader = restResultsSplit[0]
        restProjectHeader = restProjectHeader.replace('"','')
        restProjectHeaderSplit = restProjectHeader.split(',')
        #restProjectHeaderSplit = [word.replace('"', '') for word in restProjectHeader]
        
        projectNameIdx = restProjectHeaderSplit.index('name')
        projectIdx = restProjectHeaderSplit.index('ID')
        projectSecondaryIdx = restProjectHeaderSplit.index('secondary_ID')
        
        for i in xrange(1, restEndCount):
            currRow = restResultsSplit[i]
            
            currRowSplit = currRow.split(',')
            currProjectName = currRowSplit[projectNameIdx].replace('"', '')
            currProjectId = currRowSplit[projectIdx].replace('"', '')
            currProjectSecondary = currRowSplit[projectSecondaryIdx].replace('"', '')
            
            self.Projects.append(currProjectId)
            self.ProjectNames.append(currProjectName)
            self.ProjectsSecondary.append(currProjectSecondary)
            
        Projects = {'Projects':self.Projects, 'Names':self.ProjectNames, 'SecondaryName':self.ProjectsSecondary}
        return Projects
    #===============================================================================
    def getSubjects( self ):
        """Get all subjects for a given project"""
        Subjects = list()
        
        if (not self.Project):
            print 'Project is empty.  Must assign a Project before getting subjects.  Try this one ''' +self.getProjects()[0][0]+ ''
            return Subjects
#            sys.exit()
        else:
            
            restURL = self.Server + 'data/projects/' + self.Project + '/subjects?format=csv'
            restResults = self.getURLString(restURL)
            
            restResultsSplit = restResults.split('\n')
            restEndCount = restResults.count('\n')
            restSessionHeader = restResultsSplit[0]
	    restSessionHeader = restSessionHeader.replace('"','')	
            restSessionHeaderSplit = restSessionHeader.split(',')

            labelIdx = restSessionHeaderSplit.index('label')
            
            for i in range(1,restEndCount):
                currRow = restResultsSplit[i]
                
                currRowSplit = currRow.split(',')
                currSubject = currRowSplit[labelIdx].replace('"', '')
                
                Subjects.append(currSubject)
                
            #=======================================================================
            # if list is not unique, use set(Subjects)
            #=======================================================================
            return Subjects
    #===============================================================================    
    def getSubjectSessions( self ):
        """Get all sessions and session types for a given subject"""
        SubjectSessionsID = list()
        SubjectSessionUniq = list()
        SubjectSessionsType = list()
        
        if (not self.Project):
            print 'ERROR: No project specified...'
        
        AllProject = self.getProjects()
        restURL = self.Server + 'data/projects/' + self.Project + '/subjects/' + self.Subject + '/experiments?format=csv&columns=ID,label'
        restResults = self.getURLString(restURL)
        
        if (restResults != '404 Error'):
    
            restResultsSplit = restResults.split('\n')
            restEndCount = restResults.count('\n')
            restSessionHeader = restResultsSplit[0]
	    restSessionHeader = restSessionHeader.replace('"','')	
            restSessionHeaderSplit = restSessionHeader.split(',')
            
            labelIdx = restSessionHeaderSplit.index('label')
            uniqInternalId = restSessionHeaderSplit.index('ID')
            
            
            for i in xrange(1, restEndCount):
                currRow = restResultsSplit[i]
                
                currRowSplit = currRow.split(',')
                currSession = currRowSplit[labelIdx].replace('"', '')
                currSessionUniq = currRowSplit[uniqInternalId].replace('"', '')
                
                if (currSession.find('fnc') != -1) or (currSession.find('str') != -1) or (currSession.find('diff') != -1) or (currSession.find('xtr') != -1) or (currSession.find('3T') != -1):
                    if (currSession.find('xtr') != -1):
                        SubjectSessionsID.append(currSession)
                        self.Session = currSession
                        SessionTypeList = self.getSessionMeta( ).get('Types')
                        if ('T1w' in SessionTypeList):
                            SubjectSessionsType.append('strc')
                        elif ('dMRI' in SessionTypeList):
                            SubjectSessionsType.append('diff')
                        elif ('tfMRI' in SessionTypeList):
                            SubjectSessionsType.append('fnc')
                        else:
                            SubjectSessionsType.append('unknown')
                        
                    elif (currSession.find('3T') != -1):
                        
                        self.Session = currSession
                        SessionTypeList = self.getSessionMeta( ).get('Types')
                        if ('T1w' in SessionTypeList) and ('T2w' in SessionTypeList):
                            SubjectSessionsType.append('strc')
                            SubjectSessionsID.append(currSession)
                        if ('dMRI' in SessionTypeList):
                            SubjectSessionsType.append('diff')
                            SubjectSessionsID.append(currSession)
                        if ('tfMRI' in SessionTypeList):
                            SubjectSessionsType.append('fnc')
                            SubjectSessionsID.append(currSession)
                        if ('rfMRI' in SessionTypeList):
                            SubjectSessionsType.append('fnc')
                            SubjectSessionsID.append(currSession)
                            
                    else:
                        if (currSession.find('fnc') != -1): SubjectSessionsType.append('fnc')
                        elif (currSession.find('strc') != -1): SubjectSessionsType.append('strc')
                        elif (currSession.find('diff') != -1): SubjectSessionsType.append('diff')
                        else: SubjectSessionsType.append('unknown')
                        SubjectSessionsID.append(currSession)
                
            SubjectSessionUniq.append(currSessionUniq)

            SubjectSessions = {'Sessions': SubjectSessionsID, 'Types': SubjectSessionsType}
            return SubjectSessions
        else:
            print 'ERROR(getSubjectSessions()): No subject sessions found for subject %s under project %s' % (self.Subject, self.Project)
            sys.exit(-1)
    #===============================================================================    
    def getSubjectsSessions( self ):
        """Get all sessions and session types for all subjects"""
        
        if (not self.Subjects):
            print 'ERROR: No must specify a list of subjects...'
            print 'Correcting...'
            self.Subjects = self.getSubjects()
            print '...Please try again.'
        else:
            for i in xrange(0, len(self.Subjects)):
                self.Subject = self.Subjects[i]
                print self.getSubjectSessions()
                
            
    #===========================================================================
    # Session Level Meta Data
    #===========================================================================
    def getSessionMeta( self ):
        """Get ID, Type, Series, Quality, and XNAT ID for a given subject and session"""

        ScanIds = list()
        ScanTypes = list()
        ScanSeries = list()
        ScanQualty = list()
        ScanXnatId = list()

        if not self.Session:
            print 'No session for getSessionMeta()...'
            sys.exit(-1)
            
        restURL = self.Server + 'data/projects/' + self.Project + '/subjects/' + self.Subject + '/experiments/' + self.Session + '/scans?format=csv&columns=ID,type,series_description,quality,xnat:mrSessionData/id'
        
        restResults = self.getURLString(restURL)
        
        restResultsSplit = restResults.split('\n')
        restEndCount = restResults.count('\n')
        restSessionHeader = restResultsSplit[0]
	restSessionHeader = restSessionHeader.replace('"','')	
        restSessionHeaderSplit = restSessionHeader.split(',')
        

        # ['"xnat_imagescandata_id"', '"ID"', '"type"', '"series_description"', '"quality"', '"xnat:mrsessiondata/id"', '"URI"']
        idIdx = restSessionHeaderSplit.index('ID')
        seriesIdx = restSessionHeaderSplit.index('series_description')
        typeIdx = restSessionHeaderSplit.index('type')
        qualityIdx = restSessionHeaderSplit.index('quality')
        xnatidIdx = restSessionHeaderSplit.index('xnat:mrsessiondata/id')
        
        for j in xrange(1, restEndCount):
            currRow = restResultsSplit[j]
            
            currRowSplit = currRow.split(',')
    
            ScanIds.append(currRowSplit[idIdx].replace('"', ''))
            ScanTypes.append(currRowSplit[typeIdx].replace('"', ''))
            ScanSeries.append(currRowSplit[seriesIdx].replace('"', ''))
            ScanQualty.append(currRowSplit[qualityIdx].replace('"', ''))
            ScanXnatId.append(currRowSplit[xnatidIdx].replace('"', ''))
            
        SessionMeta = {'IDs':ScanIds, 'Types':ScanTypes, 'Series':ScanSeries, 'Quality':ScanQualty, 'XNATID':ScanXnatId }
        return SessionMeta
    #===============================================================================
    def getSessionQuality( self ):
        """QC: Get Session, Subject, Scan Type, Quality of all data"""

        Quality = list()
        Series = list()
        ScanIds = list()
        Sessions = list()
        ScanType = list()
        
        if (not self.Subjects):
            self.Subjects = self.getSubjects( )
        else:
            self.Subjects = self.Subject.split()
            
        for i in xrange(0, len(self.Subjects)):
            self.Subject = self.Subjects[i]
            
            if (not self.Session) and (not self.Sessions):
                self.Sessions = self.getSubjectSessions()[0]
            else:
                self.Sessions = self.Session.split()
            
            for j in xrange(0, len(self.Sessions)):
                
                self.Session = self.Sessions[j]
                
                SessionMeta = self.getSessionMeta()
                
                Quality.extend(SessionMeta.get('Quality'))
                Series.extend(SessionMeta.get('Series'))
                ScanIds.extend(SessionMeta.get('IDs'))
                ScanType.extend(SessionMeta.get('Types'))
                
                Sessions.extend( self.Session.split(',') * len(SessionMeta.get('IDs')))
                
        return Quality, ScanIds, Series, Sessions, ScanType
    #===============================================================================
    def getSubjectResources(self):
        """Get subject resources"""
        
        ResourceID = list()
        ResourceName = list()
        ResourceCategory = list()
        
        # restURL = self.Server + 'data/projects/' + self.Project + '/subjects/' + self.Subject + '/experiments/' + self.Session + '/resources?format=csv&file_stats=true'
        restURL = self.Server + 'data/projects/' + self.Project + '/subjects/' + self.Subject + '/experiments/' + self.Session + '/resources?format=csv'
        if self.Verbose: print restURL
        
        restResults = self.getURLString(restURL)
        
        if ('404 Error' in restResults):
            return restResults
            
        restResultsSplit = restResults.split('\n')
        restEndCount = restResults.count('\n')
    
        restSessionHeader = restResultsSplit[0].replace('"', '')
        restSessionHeaderSplit = restSessionHeader.split(',')
        
        xnatAbstractresourceIdIdx = restSessionHeaderSplit.index('xnat_abstractresource_id')
        labelIdx = restSessionHeaderSplit.index('label')
        elementNameIdx = restSessionHeaderSplit.index('element_name')
        categoryIdx = restSessionHeaderSplit.index('element_name')
        categoryIdIdx = restSessionHeaderSplit.index('cat_id')
        
        for i in xrange(1,restEndCount):
            currRow = restResultsSplit[i].replace('"', '')
            currRowSplit = currRow.split(',')
    
            ResourceID.append(currRowSplit[xnatAbstractresourceIdIdx])
            ResourceName.append(currRowSplit[labelIdx])
            ResourceCategory.append(currRowSplit[categoryIdx])
        
        SubjectResources = {'IDs':ResourceID, 'Names':ResourceName, 'Category':ResourceCategory }
        return SubjectResources
    #===============================================================================
    def getSubjectResourcesMeta(self):
        """Get file info about ALL resources for a subject"""
        
        ResourceHeader = list()
        FileNames = list()
        FileURIs = list()
        FileSessions = list()
        FileLabels = list()
        FileTags = list()
        FileFormats = list()
        FileContents = list()
        FileReadable = list()
        FilePath = list()
        
        SubjectSessions = list(set(self.getSubjectSessions().get('Sessions')))
    
        for i in range(0, len(SubjectSessions)):
            restURL = self.Server + 'data/projects/' + self.Project + '/subjects/' + self.Subject + '/experiments/' + SubjectSessions[i] + '/resources?format=csv'
            if self.Verbose: print restURL
            
            restResults = self.getURLString(restURL)
            
            restResultsSplit = restResults.split('\n')
            restEndCount = restResults.count('\n')
        
            restSessionHeader = restResultsSplit[0]
            restSessionHeader = restSessionHeader.replace('"','')	
            restSessionHeaderSplit = restSessionHeader.split(',')
            restSessionHeaderCount = restSessionHeader.count(',')
            
            for j in range(0, restSessionHeaderCount + 1):
                ResourceHeader.append(restSessionHeaderSplit[j].replace('"', ''))
            
            labelIdx = ResourceHeader.index('label')
            if (restEndCount > 1):
                for j in xrange(1,restEndCount):
        
                    currRow = restResultsSplit[j]
                    currRowSplit = currRow.split(',')
#                    currRowCount = currRow.count(',')
                    currLabel = currRowSplit[labelIdx].replace('"', '')
        
                    #===========================================================
                    # all this nonsense should be replaced with a call to getSubjectResourceMeta()
                    #===========================================================
                    restURL = self.Server +'data/projects/'+ self.Project +'/subjects/'+ self.Subject +'/experiments/'+ SubjectSessions[i] +'/resources/'+ currLabel +'/files?format=csv'
                    restResults = self.getURLString(restURL)
        
                    currRestResultsSplit = restResults.split('\n')
                    currRestEndCount = restResults.count('\n')
                    currRestSessionHeader = currRestResultsSplit[0]
                    currRestSessionHeader = currRestSessionHeader.replace('"','')	

                    currRestSessionHeaderSplit = currRestSessionHeader.split(',')
                    
                    nameIdx = currRestSessionHeaderSplit.index('Name')
                    sizeIdx = currRestSessionHeaderSplit.index('Size')
                    uriIdx = currRestSessionHeaderSplit.index('URI')
                    collectionIdx = currRestSessionHeaderSplit.index('collection')
                    fileTagsIdx = currRestSessionHeaderSplit.index('file_tags')
                    fileFormatIdx = currRestSessionHeaderSplit.index('file_format')
                    fileContentIdx = currRestSessionHeaderSplit.index('file_content')
        
                    for k in xrange(1,currRestEndCount):
                        newRow = currRestResultsSplit[k]
                        currRowSplit = newRow.split(',')
                        FileNames.append(currRowSplit[nameIdx].replace('"', ''))
                        FileURIs.append(currRowSplit[uriIdx].replace('"', ''))
                        FileTags.append(currRowSplit[fileTagsIdx].replace('"', ''))
                        FileFormats.append(currRowSplit[fileFormatIdx].replace('"', ''))
                        FileContents.append(currRowSplit[fileContentIdx].replace('"', ''))
                        
                        FileSessions.append(SubjectSessions[i].replace('"', ''))
                        FileLabels.append(currLabel.replace('"', ''))
                        
                    #===========================================================
                    # do the path query and check readability...    
                    #===========================================================
                    restURL = self.Server + 'data/projects/' + self.Project + '/subjects/' + self.Subject + '/experiments/' + SubjectSessions[i] + '/resources/' + currLabel + '/files?format=csv&locator=absolutePath'
                    newRestResults = self.getURLString(restURL)
        
                    newRestResultsSplit = newRestResults.split('\n')
                    newRestEndCount = newRestResults.count('\n')
                    newRestSessionHeader = newRestResultsSplit[0]
                    newRestSessionHeader = newRestSessionHeader.replace('"','')	

                    newRestSessionHeaderSplit = newRestSessionHeader.split(',')
                    
                    # ['"Name"', '"Size"', '"URI"', '"collection"', '"file_tags"', '"file_format"', '"file_content"', '"cat_ID"']
                    pathIdx = newRestSessionHeaderSplit.index('absolutePath')
                    
                    for k in xrange(1, newRestEndCount):
                        currRow = newRestResultsSplit[k]
                        currRowSplit = currRow.split(',')
                        FilePath.append(currRowSplit[pathIdx].replace('"', ''))
                        try:
                            FileObj = open(FilePath[-1], 'r')
                            # if readable:
                            FileReadable.append(True)
                        except IOError, e:
                            if self.Verbose:
                                print 'getSubjectResourcesMeta(): File read error number: %s, error code: %s, and error message: %s' % (e.errno, errno.errorcode[e.errno], os.strerror(e.errno))
                            FileReadable.append(False)

        SubjectResourcesMeta = { 'Name': FileNames, 'URI': FileURIs, 'Session': FileSessions, 'Label': FileLabels, 'Content': FileContents, 'Format': FileFormats, 'Path': FilePath, 'Readable': FileReadable }
        return SubjectResourcesMeta
    #===============================================================================  
    def getSubjectResourceMeta(self):
        """Get file info about a given resource for a subject"""
        
        Names = list()
        Sizes = list()
        URIs = list()
        Collections = list()
        RealPath = list()
        FilePath = list()
        FileTags = list()
        FileFormats = list()
        FileContents = list()
        FileReadable = list()
        
        # https://hcpx-dev-cuda00.nrg.mir/data/projects/HCP_Q1/subjects/100307/experiments/100307_3T/resources/tfMRI_WM_RL_unproc/files?format=csv&columns=ID,type,series_description,quality,xnat:mrSessionData/id
        restURL = self.Server + 'data/projects/' + self.Project + '/subjects/' + self.Subject + '/experiments/' + self.Session + '/resources/' + self.Resource + '/files?format=csv&columns=ID,type,series_description,quality,xnat:mrSessionData/id,file_tags,file_format,file_content'
        restResults = self.getURLString(restURL)
        
        if ('500 Error' in restResults):
            print 'ERROR 500: Internal Server Error in %s with URL %s' % ('getSubjectResourceMeta', restURL)
            return 500
        
        restResultsSplit = restResults.split('\n')
        restEndCount = restResults.count('\n')
        restSessionHeader = restResultsSplit[0]
	restSessionHeader = restSessionHeader.replace('"','')	
        restSessionHeaderSplit = restSessionHeader.split(',')
        
        # ['"Name"', '"Size"', '"URI"', '"collection"', '"file_tags"', '"file_format"', '"file_content"', '"cat_ID"']
        nameIdx = restSessionHeaderSplit.index('Name')
        sizeIdx = restSessionHeaderSplit.index('Size')
        uriIdx = restSessionHeaderSplit.index('URI')
        collectionIdx = restSessionHeaderSplit.index('collection')
        fileTagsIdx = restSessionHeaderSplit.index('file_tags')
        fileFormatIdx = restSessionHeaderSplit.index('file_format')
        fileContentIdx = restSessionHeaderSplit.index('file_content')
        
        
        for j in xrange(1, restEndCount):
            currRow = restResultsSplit[j]
            currRowSplit = currRow.split(',')
    
            Names.append(currRowSplit[nameIdx].replace('"', ''))
            Sizes.append(currRowSplit[sizeIdx].replace('"', ''))
            URIs.append(currRowSplit[uriIdx].replace('"', ''))
            Collections.append(currRowSplit[collectionIdx].replace('"', ''))
            FileTags.append(currRowSplit[fileTagsIdx].replace('"', ''))
            FileFormats.append(currRowSplit[fileFormatIdx].replace('"', ''))
            FileContents.append(currRowSplit[fileContentIdx].replace('"', ''))
        
        # do the path query...    
        restURL = self.Server + 'data/projects/' + self.Project + '/subjects/' + self.Subject + '/experiments/' + self.Session + '/resources/' + self.Resource + '/files?format=csv&locator=absolutePath'
        restResults = self.getURLString(restURL)
        
        restResultsSplit = restResults.split('\n')
        restEndCount = restResults.count('\n')
        restSessionHeader = restResultsSplit[0]
        restSessionHeader = restSessionHeader.replace('"','')	
        restSessionHeaderSplit = restSessionHeader.split(',')
        
        # ['"Name"', '"Size"', '"URI"', '"collection"', '"file_tags"', '"file_format"', '"file_content"', '"cat_ID"']
        pathIdx = restSessionHeaderSplit.index('absolutePath')
        
        for j in xrange(1, restEndCount):
            currRow = restResultsSplit[j]
            currRowSplit = currRow.split(',')
            FilePath.append(self.getLocalPath(currRowSplit[pathIdx].replace('"', '')))
            try:
                FileObj = open(self.getLocalPathResolved(FilePath[-1]), 'r')
                # if readable:
                FileReadable.append(True)
                RealPath.append(self.getLocalPathResolved(FilePath[-1]))
            except IOError, e:
                if self.Verbose:
                    print 'getSubjectResourceMeta(): File read error number: %s, error code: %s, and error message: %s' % (e.errno, errno.errorcode[e.errno], os.strerror(e.errno))
                FileReadable.append(False)
                RealPath.append('NA')
                
        SubjectResourceMeta = {'Name': Names, 'Bytes': Sizes, 'URI': URIs, 'Path': FilePath, 'Readable': FileReadable, 'RealPath': RealPath, 'Label': Collections, 'Format': FileFormats, 'Contents': FileContents}
        return SubjectResourceMeta
    #===============================================================================
    def getFileInfo( self, URL ):
        """Get mod-date, size, and URL for a file on the server"""

        if (URL.find('http') == -1):
            if (URL[0] == '/'):
                URL = self.Server + URL[1:-1]
            else:
                URL = self.Server + URL
            
        restRequest = urllib2.Request(URL)
        restRequest.add_header("Cookie", "JSESSIONID=" + self.SessionId);
         
        restRequest.get_method = lambda : 'HEAD'
        while (self.Timeout <= self.TimeoutMax):
            try:
                restConnHandle = urllib2.urlopen(restRequest, None)
                self.FileInfo = { 'ModDate': restConnHandle.info().getheader('Last-Modified'), 'Bytes': restConnHandle.info().getheader('Content-Length'), 'URL': URL }
            
            except HTTPError, e:
                if (e.code != 404):
                    self.Timeout += self.TimeoutStep
                    print 'HTTPError code: ' +str(e.code)+ '. Timeout increased to ' +str(self.Timeout)+' seconds for ' +URL
                else:
                    return '404 Error'
        
            if (self.FileInfo.get( 'Bytes' ) == None): 
                self.FileInfo[ 'Bytes' ] = '0'
            
            return self.FileInfo        

    #===============================================================================
    def getAssessorIDs( self ):
        """QC: Get assessor for subject and session"""

        if not (self.Project) or not (self.Subject) or not (self.Session) or not (self.AssessorDataType):
            print 'getAssessorIDs() Requirements: \n Project: %s \n Subject: %s \n Session: %s \n AssessorDataType: %s ' % (self.Project, self.Subject, self.Session, self.AssessorDataType) 
            return False
        
        if (self.Server.find('intradb') > 0):
            IDs = list()
            SessionIDs = list()
            SessionLabels = list()
            Labels = list()
            XnatIDs = list()
            URIs = list()
            XsiType = list()
                
            restURL = self.Server + 'data/projects/' + self.Project + '/subjects/' + self.Subject + '/experiments/' + self.Session + '/assessors?format=csv'
            restResults = self.getURLString(restURL)
            
            if (restResults != '404 Error'):
            
        #        AssessorSubjectSessionsList, AssessorDataTypeList = self.getSubjectSessions()
                
                restResultsSplit = restResults.split('\n')
                restEndCount = restResults.count('\n')
                restSessionHeader = restResultsSplit[0]
	        restSessionHeader = restSessionHeader.replace('"','')	
                restSessionHeaderSplit = restSessionHeader.split(',')
                
                idIdx = restSessionHeaderSplit.index('ID')
                sessionIdIdx = restSessionHeaderSplit.index('session_ID')
                sessionLabelIdx = restSessionHeaderSplit.index('session_label')
                xnatidIdx = restSessionHeaderSplit.index('xnat:imageassessordata/id')
                labelIdx = restSessionHeaderSplit.index('label')
                uriIdx = restSessionHeaderSplit.index('URI')
                xsiTypeIdx = restSessionHeaderSplit.index('xsiType')
                
                for i in xrange(1, restEndCount):
                    currRow = restResultsSplit[i]
                    currRowSplit = currRow.split(',')
                    
                    # need to call getSubjectSessions before this....
                    # self.AssessorDataType = 'qcAssessmentData'
                    if (currRowSplit[xsiTypeIdx].replace('"', '').find(self.AssessorDataType) != -1):
                    
                        IDs.append(currRowSplit[idIdx].replace('"', ''))
                        SessionIDs.append(currRowSplit[sessionIdIdx].replace('"', ''))
                        SessionLabels.append(currRowSplit[sessionLabelIdx].replace('"', ''))
                        Labels.append(currRowSplit[labelIdx].replace('"', ''))
                        XnatIDs.append(currRowSplit[xnatidIdx].replace('"', ''))
                        URIs.append(currRowSplit[uriIdx].replace('"', ''))
                        XsiType.append(currRowSplit[xsiTypeIdx].replace('"', ''))
                    
            return Labels
        else:
            print 'ERROR: Assessor data only on intradb.humanconnectome.org.'
            return -1
    #===============================================================================
    def getAssessorOutputFile( self, AssessorIDs ):
        """QC: Get assessor output files as a list"""

        AssessorOutputFileURI = list()
        AssessorOutputFileSize = list()
        
        for i in xrange(0, len(AssessorIDs)):
            currID = AssessorIDs[i]
            
            restURL = self.Server + 'data/projects/' + self.Project + '/subjects/' + self.Subject + '/experiments/' + self.Session + '/assessors/' + currID + '/files?format=csv'
            restResults = self.getURLString(restURL)
            
            restResultsSplit = restResults.split('\n')
            restEndCount = restResults.count('\n')
            restSessionHeader = restResultsSplit[0]
            restSessionHeader = restSessionHeader.replace('"','')	

            restSessionHeaderSplit = restSessionHeader.split(',')
            
            #===================================================================
            # Hopefully, digest will come out here?
            # digestIdx = restSessionHeaderSplit.index('Digest')
            # "Name","Size","URI","collection","file_tags","file_format","file_content","cat_ID"
            #===================================================================
            # Maybe useful later...
            #===================================================================
            # nameIdx = restSessionHeaderSplit.index('Name')
            # collectionIdx = restSessionHeaderSplit.index('collection')
            # fileTagsIdx = restSessionHeaderSplit.index('file_tags')
            # fileFormatIdx = restSessionHeaderSplit.index('file_format')
            # fileContentIdx = restSessionHeaderSplit.index('file_content')
            # catIdIdx = restSessionHeaderSplit.index('cat_ID')     
            #===================================================================
            sizeIdx = restSessionHeaderSplit.index('Size')
            uriIdx = restSessionHeaderSplit.index('URI')      
           
            for i in xrange(1, restEndCount):
                currRow = restResultsSplit[i]
                currRowSplit = currRow.split(',')
                AssessorOutputFileURI.append(currRowSplit[uriIdx].replace('"', ''))
                AssessorOutputFileSize.append(currRowSplit[sizeIdx].replace('"', ''))
                        
        return AssessorOutputFileURI
    #===============================================================================
    def getScanParms( self ):
        """HCP: Get scan parms from a scan, duh."""
        # def getScanParms(inputUser, inputPassword, inputProject, inputSubject, inputSession, inputScan):

        restURL = self.Server + 'data/projects/' +self.Project+ '/subjects/' +self.Subject+ '/experiments/' +self.Session+ '/scans/' +self.Scan + '?format=xml'
        xmlData = self.getURLString( restURL )
        parmsET = ET.fromstring( xmlData )
        
        acquisitionTime = parmsET.find('{http://nrg.wustl.edu/xnat}startTime').text
        acquisitionDay = parmsET.find('{http://nrg.wustl.edu/xnat}sessionDay').text
        
        scanParms = parmsET.find('{http://nrg.wustl.edu/xnat}parameters')
        sampleSpacing = scanParms.find('{http://nrg.wustl.edu/xnat}readoutSampleSpacing').text
        voxelResolution = scanParms.find('{http://nrg.wustl.edu/xnat}voxelRes').attrib
        orientation = scanParms.find('{http://nrg.wustl.edu/xnat}orientation').text
        FOV = scanParms.find('{http://nrg.wustl.edu/xnat}readoutSampleSpacing').text
        TR = scanParms.find('{http://nrg.wustl.edu/xnat}tr').text
        
        flipAngle = scanParms.find('{http://nrg.wustl.edu/xnat}flip').text
        scanSequence = scanParms.find('{http://nrg.wustl.edu/xnat}scanSequence').text
        pixelBandwidth = scanParms.find('{http://nrg.wustl.edu/xnat}pixelBandwidth').text
        
        # alt parms that are not present in all scan types...
        try:
            readoutDirection = scanParms.find('{http://nrg.wustl.edu/xnat}readoutDirection').text
        except:
            readoutDirection = 'NA'
        try:
            echoSpacing = scanParms.find('{http://nrg.wustl.edu/xnat}echoSpacing').text
        except:
            echoSpacing = 'NA'
        try:
            peDirection = scanParms.find('{http://nrg.wustl.edu/xnat}peDirection').text
            # Here be a hack for the +x, x+ stuff...
            if ('+' in peDirection):
                peDirection = peDirection.replace('+', '')
        except:
            peDirection = 'NA'
        try:
            shimGroup = scanParms.find('{http://nrg.wustl.edu/xnat}shimGroup').text
        except:
            shimGroup = 'NA'
        try:
            seFieldMapGroup = scanParms.find('{http://nrg.wustl.edu/xnat}seFieldMapGroup').text
        except:
            seFieldMapGroup = 'NA'
        try:
            deltaTE = scanParms.find('{http://nrg.wustl.edu/xnat}deltaTE').text
        except:
            deltaTE = 'NA'
        try:
            TE = scanParms.find('{http://nrg.wustl.edu/xnat}te').text
        except:
            TE = 'NA'
        try:
            GEFieldMapGroup = scanParms.find('{http://nrg.wustl.edu/xnat}geFieldMapGroup').text
        except:
            GEFieldMapGroup = 'NA'
        
        try:
            biasGroup = scanParms.find('{http://nrg.wustl.edu/xnat}biasGroup').text
        except:
            biasGroup = 'NA'
        
        for addParms in scanParms.findall('{http://nrg.wustl.edu/xnat}addParam'):
            addParmsAttrib = addParms.attrib
            
            if (addParmsAttrib.get('name') == 'Siemens GRADSPEC alShimCurrent'):
                alShimCurrent = addParms.text
                
            if (addParmsAttrib.get('name') == 'Siemens GRADSPEC lOffset'):
                LinOffset = addParms.text
        
        scanParms = { 'SampleSpacing': sampleSpacing, 'alShimCurrent': alShimCurrent, 'LinearOffset':  LinOffset, 'AcquisitionTime': acquisitionTime, 'VoxelResolution': voxelResolution, 'Orientation': orientation, \
                            'FOV': FOV, 'TR': TR, 'TE': TE, 'FlipAngle': flipAngle, 'ScanSequence': scanSequence, 'PixelBandwidth': pixelBandwidth, 'ReadoutDirection': readoutDirection, 'EchoSpacing': echoSpacing, \
                            'PhaseEncodingDir': peDirection, 'ShimGroup': shimGroup, 'SEFieldMapGroup': seFieldMapGroup, 'DeltaTE': deltaTE, 'GEFieldMapGroup': GEFieldMapGroup, 'SessionDay': acquisitionDay, \
                            'BiasGroup': biasGroup }
        return scanParms
    #===============================================================================    
    def getScanMeta( self ):
        """Get Scan ID, Type, Series, Quality, and XNAT ID for a given subject and session"""

        Names = list()
        Sizes = list()
        URIs = list()
        Collections = list()
        FilePath = list()
        FileTags = list()
        FileFormats = list()
        FileContents = list()
        FileReadable = list()

        if (not self.Scan):
            print 'Scan not defined...'
        else:
            restURL = self.Server + 'data/projects/' + self.Project + '/subjects/' + self.Subject + '/experiments/' + self.Session + '/scans/' + self.Scan + '/files?format=csv&columns=ID,type,series_description,quality,xnat:mrSessionData/id'

        restResults = self.getURLString(restURL)
        
        restResultsSplit = restResults.split('\n')
        restEndCount = restResults.count('\n')
        restSessionHeader = restResultsSplit[0]
	restSessionHeader = restSessionHeader.replace('"','')	
        restSessionHeaderSplit = restSessionHeader.split(',')
        
        # ['"Name"', '"Size"', '"URI"', '"collection"', '"file_tags"', '"file_format"', '"file_content"', '"cat_ID"']
        nameIdx = restSessionHeaderSplit.index('Name')
        sizeIdx = restSessionHeaderSplit.index('Size')
        uriIdx = restSessionHeaderSplit.index('URI')
        collectionIdx = restSessionHeaderSplit.index('collection')
        fileTagsIdx = restSessionHeaderSplit.index('file_tags')
        fileFormatIdx = restSessionHeaderSplit.index('file_format')
        fileContentIdx = restSessionHeaderSplit.index('file_content')
        
        for j in xrange(1, restEndCount):
            currRow = restResultsSplit[j]
            currRowSplit = currRow.split(',')
    
            Names.append(currRowSplit[nameIdx].replace('"', ''))
            Sizes.append(currRowSplit[sizeIdx].replace('"', ''))
            URIs.append(currRowSplit[uriIdx].replace('"', ''))
            Collections.append(currRowSplit[collectionIdx].replace('"', ''))
            FileTags.append(currRowSplit[fileTagsIdx].replace('"', ''))
            FileFormats.append(currRowSplit[fileFormatIdx].replace('"', ''))
            FileContents.append(currRowSplit[fileContentIdx].replace('"', ''))
        
        # do the path query...    
        restURL = self.Server + 'data/projects/' + self.Project + '/subjects/' + self.Subject + '/experiments/' + self.Session + '/scans/' + self.Scan + '/files?format=csv&locator=absolutePath'
        restResults = self.getURLString(restURL)
        
        restResultsSplit = restResults.split('\n')
        restEndCount = restResults.count('\n')
        restSessionHeader = restResultsSplit[0]
        restSessionHeader = restSessionHeader.replace('"','')	

        restSessionHeaderSplit = restSessionHeader.split(',')
        
        # ['"Name"', '"Size"', '"URI"', '"collection"', '"file_tags"', '"file_format"', '"file_content"', '"cat_ID"']
        pathIdx = restSessionHeaderSplit.index('absolutePath')
        
        for j in xrange(1, restEndCount):
            currRow = restResultsSplit[j]
            currRowSplit = currRow.split(',')
            FilePath.append(self.getLocalPath(currRowSplit[pathIdx].replace('"', '')))
            try:
                FileObj = open(FilePath[-1], 'r')
                # if readable:
                FileReadable.append(True)
            except IOError, e:
                if self.Verbose:
                    print 'getScanMeta(): File read error number: %s, error code: %s, and error message: %s' % (e.errno, errno.errorcode[e.errno], os.strerror(e.errno))
                FileReadable.append(False)
            
        ScanMeta = {'Name': Names, 'Bytes': Sizes, 'URI': URIs, 'Path': FilePath, 'Readable': FileReadable, 'Collections': Collections, 'Format': FileFormats, 'Content': FileContents }
        return ScanMeta
    #===============================================================================    
    def getSubjectMeta( self ):
        """Get Subject Metadata"""
        
        TagList = list()
        ValueList = list()
        self.Session = '%s_%s' % (self.Subject, 'SubjMeta')
        
        if (not self.Session):
            print 'Session not defined...'
        else:
            restURL = self.Server + 'data/projects/' + self.Project + '/subjects/' + self.Subject + '/experiments/' + self.Session + '?format=xml'

            xmlData = self.getURLString( restURL )
            parmsET = ET.fromstring( xmlData )
            
            namespace = 'http://nrg.wustl.edu/hcp'
            completenessNode = parmsET.find(str(QName( namespace, 'completeness' )))
            imagingNode = completenessNode.find(str(QName( namespace, 'imaging' )))
            
            for children in imagingNode:
                childTag = children.tag
                childText = children.text
                childTagSplit = childTag.split('}')
                
                #===============================================================
                # if (childText == '0'): childText = False
                # elif (childText == '1'): childText = True
                #===============================================================
                
                TagList.append(childTagSplit[-1])
                ValueList.append(childText)
                
            SubjectMeta = dict(zip(TagList, ValueList))
            return SubjectMeta
    #===============================================================================    

    def getLocalPath(self, archivePath):
        """Translate catalog path to local path for cross mounted folder"""
        indexPathReplacementSeparator=hcp_constants.HCP_PATH_PREFIX.find(hcp_constants.HCP_PATH_PREFIX_SEPERATOR)
        if (indexPathReplacementSeparator != -1):
           afterSeperatorIndex=indexPathReplacementSeparator+1
           archive_prefix=hcp_constants.HCP_PATH_PREFIX[:indexPathReplacementSeparator]
           local_prefix=hcp_constants.HCP_PATH_PREFIX[afterSeperatorIndex:]
           localPath=archivePath.replace(archive_prefix,local_prefix)
           return localPath
        else:
           return archivePath

    #===============================================================================    

    def getLocalPathResolved(self, archivePath):
        """Translate catalog path to local path for cross mounted folder"""
        indexPathReplacementSeparator=hcp_constants.HCP_PATH_PREFIX.find(hcp_constants.HCP_PATH_PREFIX_SEPERATOR)
        if (indexPathReplacementSeparator != -1):
           afterSeperatorIndex=indexPathReplacementSeparator+1
           archive_prefix=hcp_constants.HCP_PATH_PREFIX[:indexPathReplacementSeparator]
           local_prefix=hcp_constants.HCP_PATH_PREFIX[afterSeperatorIndex:]
           localPath=archivePath.replace(archive_prefix,local_prefix)
	   realPath=os.path.realpath(localPath)
	   if (realPath != localPath):
	     localPath=self.getLocalPath(realPath)
           return localPath
        else:
           return archivePath
           
    #===============================================================================
    # WORKFLOW
    #===============================================================================  
    #===============================================================================  
    def getParsedWorkflow( self ):
        """Get Workflow Data and Parse"""
    
        # https://db.humanconnectome.org/data/services/workflows/FunctionalHCP?columns=functionalseries,builddir&format=csv&latest_by_param=functionalseries
        # "label","label","id","externalid","pipeline_name","launch_time","jobid","status","current_step_launch_time","current_step_id","builddir"
        Subject = list()
#        Session = list()
        ID = list()
#        ExternalID = list()
        PipelinePathName = list()
        LaunchTime = list()
        JobID = list()
        JobStatus = list()
        StepLaunchTime = list()
        StepID = list()
        BuildDir = list()
        FunctionalSeries = list()


        if (self.Pipeline == 'FunctionalHCP'):
            restURL = self.Server + 'data/services/workflows/' + self.Pipeline + '?columns=functionalseries,builddir&format=csv&latest_by_param=functionalseries'
        else:
            restURL = self.Server + 'data/services/workflows/' + self.Pipeline + '?display=LATEST&columns=builddir&format=csv'
            
        restData = self.getURLString( restURL )
    
        
        restResultsSplit = restData.split('\n')
        restEndCount = restData.count('\n')
        restSessionHeader = restResultsSplit[0].replace('"', '')
        restSessionHeaderSplit = restSessionHeader.split(',')
        
        labelIdx = restSessionHeaderSplit.index('label')
        idIdx = restSessionHeaderSplit.index('id')
        pipelineIdx = restSessionHeaderSplit.index('pipeline_name')
        launchTimeIdx = restSessionHeaderSplit.index('launch_time')
        jobIdx = restSessionHeaderSplit.index('jobid')
        statusIdx = restSessionHeaderSplit.index('status')
        stepLaunchIdx = restSessionHeaderSplit.index('current_step_launch_time')
        stepIdx = restSessionHeaderSplit.index('current_step_id')
        if (self.Pipeline == 'FunctionalHCP'):
            functionalSeriesIdx = restSessionHeaderSplit.index('functionalseries')
        buildDirIdx = restSessionHeaderSplit.index('builddir')
        
        for j in xrange(1, restEndCount):
            currRow = restResultsSplit[j]
            
            currRowSplit = currRow.split(',')
    
            Subject.append(currRowSplit[labelIdx].replace('"', ''))
            ID.append(currRowSplit[idIdx].replace('"', ''))
            PipelinePathName.append(currRowSplit[pipelineIdx].replace('"', ''))
            LaunchTime.append(currRowSplit[launchTimeIdx].replace('"', ''))
            JobID.append(currRowSplit[jobIdx].replace('"', ''))
            JobStatus.append(currRowSplit[statusIdx].replace('"', ''))
            StepLaunchTime.append(currRowSplit[stepLaunchIdx].replace('"', ''))
            StepID.append(currRowSplit[stepIdx].replace('"', ''))
            if (self.Pipeline == 'FunctionalHCP'):
                FunctionalSeries.append(currRowSplit[functionalSeriesIdx].replace('"', ''))
            BuildDir.append(currRowSplit[buildDirIdx].replace('"', ''))
            
        # a short, ugly, sorting subroutine...surely there is something better...
        s = Subject
        sortIdx = map(int, sorted(range(len(s)), key=lambda k: s[k]))
        
        Subject = [Subject[i] for i in sortIdx]
        PipelinePathName = [PipelinePathName[i] for i in sortIdx]
        LaunchTime = [LaunchTime[i] for i in sortIdx]
        JobID = [JobID[i] for i in sortIdx]
        JobStatus = [JobStatus[i] for i in sortIdx]
        StepLaunchTime = [StepLaunchTime[i] for i in sortIdx]
        StepID = [StepID[i] for i in sortIdx]
        BuildDir = [BuildDir[i] for i in sortIdx]
        FunctionalSeries = [FunctionalSeries[i] for i in sortIdx]

        
        ParsedData = {'Subject': Subject, 'ID': ID, 'PipelinePathName': PipelinePathName, 'LaunchTime': LaunchTime, 'JobID': JobID, 'JobStatus': JobStatus, 'StepLaunchTime': StepLaunchTime, 'StepID': StepID, 'BuildDir': BuildDir, 'FunctionalSeries': FunctionalSeries}
        return ParsedData
#===============================================================================    
#===============================================================================
# def fPrint( outputDirFile, headerStr, *args ):
# 
#    outputFile = os.path.basename(outputDirFile)
#    ouputFileBase, outputFileExt = os.path.splitext(outputFile)
#    outputDir = os.path.dirname(os.path.normpath(outputDirFile)) + os.sep
# 
#    if not os.path.exists(outputDir):
#        os.makedirs(outputDir)
#        
#    fileID = open(outputDirFile, 'wb')
#        
#    for i in xrange(0, len(headerStr)):
#        if (i < len(headerStr)-1):
#            fileID.write(headerStr[i]+'\t')
#        else:
#            fileID.write(headerStr[i]+'\n')
#            
#    for i in xrange(0, len(args[0])):
#        for j in xrange(0, len(args)):
#            
#            if (j < len(args)-1):
#                fileID.write('%s' % args[j][i] + "\t")
#            else:
#                fileID.write('%s' % args[j][i] + "\n")
#===============================================================================
#===============================================================================
        
#===============================================================================
# WRITE
#===============================================================================
class writeHCP(getHCP):
    """HCP Write Class"""
    def __init__( self, getHCP, DestinationDir  ):
        self.DestinationDir = DestinationDir
        self.Server = getHCP.Server
        self.SessionId = getHCP.SessionId
        self.Timeout = getHCP.Timeout
        self.TimeoutMax = getHCP.TimeoutMax
        self.TimeoutStep = getHCP.TimeoutStep
        self.FileInfo = getHCP.FileInfo
        self.Verbose = getHCP.Verbose
        self.Flatten = False
        
        self.BytesStream = list()
        self.BytesWrite = list()
        
    #===============================================================================
    def getURLString(self, fileURL):
        return super(writeHCP, self).getURLString(fileURL)
    #===============================================================================
    def getURLData(self, fileURL):
        return super(writeHCP, self).getURLData(fileURL)

    #===============================================================================
    def getFileInfo(self, fileURL):
        return super(writeHCP, self).getFileInfo(fileURL)
    #===============================================================================
    def writeFileFromURL( self, getHCP, FileURI, FileName ):
    
        try:
            FileURIList = FileURI.split(',')
        except:
            FileURIList = FileURI
        try:
            FileNameList = FileName.split(',')
        except:
            FileNameList = FileName

        
        WriteCode = True
        if (self.DestinationDir[-1] != os.sep):
            self.DestinationDir = self.DestinationDir + os.sep

        if not os.path.exists(self.DestinationDir):
            os.makedirs(self.DestinationDir)
            
        for i in xrange(len(FileURIList)):
            currURI = FileURIList[i]
            currURISplit = currURI.split('/')
            currFileNameIdx = currURISplit.index(os.path.basename(currURI))
            currResrouceRootIdx = currURISplit.index('files') + 1
            
            if not self.Flatten:
                if (currFileNameIdx > currResrouceRootIdx):
                    newDestinationDir = self.DestinationDir +os.sep.join(currURISplit[currResrouceRootIdx:currFileNameIdx])+os.sep
                    
                    if not os.path.exists(newDestinationDir):
                        os.makedirs(newDestinationDir)
            else:
                newDestinationDir = self.DestinationDir

                
            if (FileName == None) or (not FileName):
                currFileName = os.path.basename(currURI)
            else:
                currFileName = FileNameList[i]
                
            # if currURI has preceeding slash, get rid of it because Server ends in slash by cleanup after init...
            if (currURI[0] == '/'):
                currURI = currURI[1:]
                
            fileURL = self.Server + currURI
            fileInfo = self.getFileInfo(fileURL)
            
            try:
                fileSize = os.path.getsize(newDestinationDir + currFileName)
            except:
                fileSize = 0
                
            if (fileInfo.get('Bytes') != str(fileSize)):
            
                fileResults = getHCP.getURLData(fileURL)
                self.BytesStream.append(len(fileResults))
                
                if (fileInfo.get('Bytes') != str(len(fileResults))):
                    print 'WARNING: Expected ' +fileInfo.get('Bytes')+ ' bytes and downloaded ' +str(len(fileResults))+ ' bytes for file ' +currFileName
                    WriteCode = False
                else:
                    with open(newDestinationDir + currFileName, 'wb') as outputFileObj:
                        writeCode = outputFileObj.write(fileResults)
                        if (self.Verbose):
                            print 'File: ' +newDestinationDir+currFileName+ '  Write Code: ' +str(writeCode)
                        outputFileObj.flush()
                        os.fsync(outputFileObj)
                        outputFileObj.close()
                        
                    # check file size after write...
                    writeFileSize = os.path.getsize(newDestinationDir + currFileName)
                    self.BytesWrite.append(writeFileSize)
                    
                    if (fileInfo.get('Bytes') != str(writeFileSize)):
                        print 'WARNING: WROTE ' +str(len(fileResults))+ ' bytes but expected ' +str(writeFileSize)+ ' bytes for file ' +newDestinationDir+currFileName
                        WriteCode = False
            else:
                print 'File %s already exists...' % (newDestinationDir + currFileName)
                self.BytesStream.append(0)
                self.BytesWrite.append(0)
                    
        return WriteCode
    #===============================================================================
    def writeFileFromPath( self, FilePathName, FileName ):
        
        try:
            FilePathNameList = FilePathName.split(',')
        except:
            FilePathNameList = FilePathName
            
        try:
            FileNameList = FileName.split(',')
        except:
            FileNameList = FileName
       
        WriteCode = True
        if (self.DestinationDir[-1] != os.sep):
            self.DestinationDir = self.DestinationDir + os.sep

        if not os.path.exists(self.DestinationDir):
            os.makedirs(self.DestinationDir)
        
        for i in xrange(len(FilePathNameList)):
            currFilePathName = FilePathNameList[i]
            
            currFilePathNameSplit = currFilePathName.split('/')
            currFileNameIdx = currFilePathNameSplit.index(os.path.basename(currFilePathName))
            try: 
                #===============================================================
                # CAUTION HERE...
                #===============================================================
#                currResourceRootIdx = currFilePathNameSplit.index('RESOURCES') + 1
                currResourceRootIdx = currFilePathNameSplit.index('RESOURCES') + 2
            except:
                currResourceRootIdx = currFileNameIdx
            
            if not self.Flatten:
                if (currFileNameIdx > currResourceRootIdx):
#                    print self.DestinationDir +os.sep.join(currFilePathNameSplit[currResourceRootIdx:currFileNameIdx])+os.sep
                    newDestinationDir = self.DestinationDir +os.sep.join(currFilePathNameSplit[currResourceRootIdx:currFileNameIdx])+os.sep
                    
                    if not os.path.exists(newDestinationDir):
                        os.makedirs(newDestinationDir)
            else:
                newDestinationDir = self.DestinationDir
            
            if (not FileName):
                currFileName = os.path.basename(currFilePathName)
            else:
                currFileName = FileNameList[i]
            
            WriteCode = subprocess.call(('cp %s %s' % (currFilePathName, newDestinationDir + currFileName)), shell=True)
            self.BytesWrite.append(os.path.getsize(newDestinationDir + currFileName))
        
        return WriteCode
#===============================================================================
# END CLASS DEFs
#===============================================================================
    
if __name__ == "__main__":
    pyHCP(sys.argv[1], sys.argv[2], sys.argv[3])





