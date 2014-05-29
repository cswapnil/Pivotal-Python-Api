import urllib2
from urllib2 import URLError
from xml.etree import ElementTree
from xml.dom.minidom import parseString

##HELPER FUNCTIONS - COULD BE USED BY ANY CLASS IN THIS FILE
def remove_non_ascii(s):
        return "".join(filter(lambda x: ord(x)<128, s))

def dict2xml(d,parent=None):
        if parent is None:
            parent = ElementTree.Element('story')

        for key, value in d.items():
            if isinstance(value, str):
                element = ElementTree.SubElement(parent, key)
                element.text = value
            elif isinstance(value, int):
                element = ElementTree.SubElement(parent, key)
                element.set('type','integer')
                element.text = str(value)
            elif isinstance(value, dict):
                element = ElementTree.SubElement(parent, key)
                dict2xml(value, element)
            elif isinstance(value, list):
                for text in value:
                    element = ElementTree.SubElement(parent, key)
                    element.text = str(text)
            else:
                raise TypeError('Unexpected value type: {0}'
                                .format(type(value)))
        return parent

def issue_post_request(url,data,headers):
    request = urllib2.Request(url,data,headers)
    try:
##                Open the URL Request
        response = urllib2.urlopen(request)
        return response.read()
        response.close()
    except URLError, e:
        if hasattr(e,'reason'):
            print 'Failed to reach the server'
            print 'Reason:',e.reason
        elif hasattr(e,'code'):
            print 'Server could not fulfil the request'
            print 'Error code:',e.code
        else:
            print 'Nothing wrong found'

##
## Pivotal Class to handle adding stories in the Tracker.
##            Members
##            api_id - The API ID provided by Pivotal
##            project_id - The project ID in which the stories need to be inserted
##                         This field is default '0' and can be set to correct value
##                         after the Pivotal object creation.
##            story - A object of type Story which will be inserted in the Pivotal project
##            api_version - The API Version to determine whether to use V2 API(XML Based)
##                          or V3 API(JSON Based).
##
class Pivotal:
    def __init__(self,api_id=None,project_id=0,story=[],api_version=2):
        self.api_id = api_id
        self.project_id = project_id
        self.story = story
        if self.project_id != 0:
            self.url = "https://www.pivotaltracker.com/services/v3/projects/%d/stories"%self.project_id
        else:
            self.url = ""
        self.api_version = api_version
        if api_version == 3:
            self.content_type = 'application/json'
        else:
            self.content_type = 'application/xml'
        self.headers = {"X-TrackerToken":self.api_id,"Content-Type":self.content_type}
            
##Setters and Getters for API ID
    def setApiId(self,api_id):
        self.api_id = api_id

    def getApiId(self):
        return self.api_id

##Setters and Getters for Projects
    def setProject(self,project_id):
        self.project_id = project_id

    def getProject(self):
        return self.project_id

##Setters and Getters for Story Object
    def addAStory(self,story):
        self.story.append(story)

    def getStories(self):
        return self.story

##Setters and Getters for Headers
    def addToHeaders(self,key,value):
        self.headers[key]=value

    def getHeaders(self):
        return self.headers

##Setters and Getters for URL
    def updateURL(self,url):
        self.url = url

    def getURL(self):
        return self.url

##Module to insert a story in Pivotal using the URLLIB API
    def insertTheStory(self,story):
        data = {'story_type':story.story_type,'name':str(remove_non_ascii(story.story_name)),'labels':str(remove_non_ascii(story.story_labels)),'description':str(remove_non_ascii(story.story_description)),'current_state':story.story_state}
        if self.api_version == 2:
            xml_data=ElementTree.tostring(dict2xml(data))
        else:
            xml_data=data
        response = issue_post_request(self.url,xml_data,self.headers)
        if self.api_version == 2:
            dom = parseString(response)
            xmlTag = dom.getElementsByTagName('id')[0].toxml()
            xmlData= xmlTag.replace('<id type="integer">','').replace('</id>','')
            story.story_id = int(xmlData)
##        else:
##            Not Implemented Yet

    def updateTheStory(self,story):      
        if story.note is None:
            if story.task is None:
                print "Either Note or Task should be give ... skipping!!!"
            else:
                data = {'description':str(remove_non_ascii(story.task))}
                parent = 'task'
                url = "https://www.pivotaltracker.com/services/v3/projects/%d/stories/%d/tasks"%(self.project_id,story.story_id)
        else:
            data = {'text':str(remove_non_ascii(story.note))}
            parent = 'note'
            url = "https://www.pivotaltracker.com/services/v3/projects/%d/stories/%d/notes"%(self.project_id,story.story_id)
            
        if self.api_version == 2:
            node_parent = ElementTree.Element(parent)
            xml_data = ElementTree.tostring(dict2xml(data,node_parent))
##        else:
##            NOT YET IMPLEMENT
        issue_post_request(url,xml_data,self.headers)
        

##PERFORM ALL THE OUTSTANDING TASKS
    def pivotalRefresh(self):
        for story in self.story:
            if story.update_only is True:
                self.updateTheStory(story)
            else:
                self.insertTheStory(story)
        print "Inserted %d stories in this session"%len(self.story)

##    
##    Story Class to store all the attributes related to a story    
##
class Story:
    __story_count = 0;
    def __init__(self,story_name,story_opt_number=0,story_type='bug',story_description='new story',story_state='unscheduled',story_id=0,story_labels='',update_only=False,note=None,task=None):
        self.story_name = story_name
        self.story_type = story_type
        self.story_description = story_description
        self.story_state = story_state
        self.story_id = story_id
        self.story_labels = story_labels
        self.update_only = update_only
        self.note = note
        self.task = task
        self.story_opt_number = int(story_opt_number)
        Story.__story_count = Story.__story_count + 1

    def getStoryName(self):
        return self.story_name

    def setStoryType(self,story_type):
        self.story_type = story_type

    def getStoryType(self):
        return self.story_type

    def setStoryDescription(self,story_description):
        self.story_description = story_description

    def getStoryDescription(self):
        return self.story_description

    def setStoryState(self,state):
        self.story_state = state

    def getStoryState(self):
        return self.story_state

##Setters and Getters for Stories
    def setStoryId(self,story_id):
        self.story_id = story_id

    def getStoryId(self):
        return self.story_id

    def getStoryOptNumber(self):
        return self.story_opt_number

    def displayTotalStories(self):
        print "Total Stories %d" %Story.__story_count
        
        
        
