Pivotal-Python-Api
==================

A API for interacting with Pivotal Tracker using their XML based API.

Starting to use.


1. Instantiate Pivotal Object -
	piv = Pivotal('#PIVOTAL_API_ID',#PROJECT_ID)

2. Create a Story Object
	story = Story('test1')
	where the name of the story is only required parameter.
	Rest of the optional parameters that can be set while 		creating a story are:
		story_type
		story_desription
		story_state
		story_id
		story_labels

	Two types of Story objects can be created.
	One to create a new story which can have all the 		attributes except update_only = false, and note,task are 	None.
	Second to create a update only story which can update the 	Note or Task of a particular story in which the Story ID 	in pivotal is required and rest fields are dont care.


3. Add stories to the Pivotal object
	piv.addAStory(story)

4. Repeat steps 2 &3 for as many stories that need to be added

5. Finally refresh the pivotal
     piv.pivotalRefresh()

   All stories will end up in the Pivotal

Story -
Active Functions
    setStoryId(story_id)
    setStoryType(story_type)
    setStoryDescription(story_description)
    setStoryState(state)

Passive Functions
    getStoryName()
    getStoryType()
    getStoryDescription()
    getStoryState()
    getStoryId()

Pivotal -
Active Functions
     setApiId(api_id)
     setProject(project_id)
     addAStory(story)

Passive Functions
     getApiId()
     getProject()
     getStories()
