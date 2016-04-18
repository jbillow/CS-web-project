# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db

# session code from this example:
# url: http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html

import jinja2
import webapp2
from webapp2_extras import sessions

# import functions

import funcs


# boiler plate code for sessions
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

# more boiler plate code
class BaseHandler(webapp2.RequestHandler):  # Copied from Google's doc
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class Profile(db.Model):
    petName = db.StringProperty(required=True)
    dose = db.FloatProperty(required=True)
    timeStamp = db.DateTimeProperty(auto_now=True)
    submitter = db.UserProperty()

# [START main_page]
class MainPage(BaseHandler):

    def get(self):

        medList = ["Medicine info"]
        self.session['medList'] = medList
        
        petList = db.GqlQuery("SELECT * FROM Profile ORDER BY timeStamp")
        doseList = db.GqlQuery("SELECT * FROM Profile ORDER BY timeStamp")
        
        template_values={'pets':petList,'dose':doseList}
        
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]

class CreateController(BaseHandler):

    def get(self):
        #get html form info
        user = users.get_current_user()
        pet = self.request.get("pet")
        weight = self.request.get("weight")
        conc = self.request.get("concentration")
        medType = self.request.get("meds")
        #convert medicine to number for use in functions
        if medType == 'doxycycline':
            medType = 1
        elif medType == 'amoxicillin':
            medType = 2
        elif medType == 'baytril':
            medType = 3
        weight = float(weight)
        conc = float(conc)
        #to calculate the dose
        doseType = funcs.calculateDose(weight,conc,medType)
        #query the datbase 
        petList = db.GqlQuery("SELECT * FROM Profile WHERE submitter =:1 ORDER BY timeStamp",user).fetch(100000)
        doseList = db.GqlQuery("SELECT * FROM Profile WHERE submitter =:1 ORDER BY timeStamp",user).fetch(100000)
        profile = Profile(dose=doseType,petName=pet)
        profile.submitter = user
        profile.put()
        petList.append(pet)
        doseList.append(doseType)
        #get and set session object
        medList = self.session['medList']
        medList.append(medType)
        self.session['medList'] = medList

    	template_values = {'pets':petList,'dose':doseList}
    	

        template = JINJA_ENVIRONMENT.get_template('form.html')
        self.response.write(template.render(template_values))

class formController(BaseHandler):

    def get(self):
        #load calculate page after navigating away from the page or for the first time
        user = users.get_current_user()
        petList = db.GqlQuery("SELECT * FROM Profile WHERE submitter =:1 ORDER BY timeStamp",user).fetch(100000)
        doseList = db.GqlQuery("SELECT * FROM Profile WHERE submitter =:1 ORDER BY timeStamp",user).fetch(100000)
       
        template_values = {'pets':petList,'dose':doseList}
        
        template = JINJA_ENVIRONMENT.get_template('form.html')
        self.response.write(template.render(template_values))


class infoController(BaseHandler):

    def get(self):
        #get session object
        medList = self.session['medList']
        #get the last index 
        medCurrent = medList[-1]
        #get info
        medInfo = funcs.getMedInfo(medCurrent)

        template_values = {'med':medInfo}
        
        template = JINJA_ENVIRONMENT.get_template('info.html')
        self.response.write(template.render(template_values))

# boiler plate
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}


# map url requests to handlers
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/on_create', CreateController),
    ('/info', infoController),
    ('/create', formController),
], config=config, debug=True)
