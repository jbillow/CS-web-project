from google.appengine.api import users
from google.appengine.ext import db

class Profile(db.Model):
    petName = db.StringProperty(required=True)
    dose = db.FloatProperty(required=True)
    timeStamp = db.DateTimeProperty(auto_now=True)
    submitter = db.UserProperty()

def calculateDose(weight, concentration, medicine):
	
	if medicine == 1:
		#2.5 mg/lb
		dose = 2.5
		mL = (weight * dose)/concentration
	
	else: 
		#10 mg/lb
		dose = 10.0
		mL = (weight * dose)/concentration
	
	return mL

def getMedInfo(medicine):
	
	info = "Info will display here after you submit a calculation"
	
	if medicine == 1:
		info = "Doxycycline medicine info:\n Works well against Mycoplasma in rats and other respiratory diseases but not much else.\nWorks well along with enrofloxacin and should not be used with pregnant or nursing moms.\n"

	elif medicine == 2:
		info = "Amoxicillin medicine info:\n Amoxicillin has a wide variety of uses.\nIt is often used to prevent and treat infections found in cuts and wounds,/nthe mouth, the upper respiratory system, and the bladder.\n Amoxicillin is one of the only antibiotics that is\n perfectly safe to give to pregnant and nursing mothers and babies of any age.\n It can also be given alongside enrofloxacin or doxycycline.\n"

	elif medicine == 3:
		info = "Baytril medicine info:\n Enrofloxacin is a broad spectrum antibiotic\n used in veterinary medicine to treat animals afflicted with certain bacterial infections\n It should not be used in young animals\n"

	return info