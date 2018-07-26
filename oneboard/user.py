import os
import pickle
from recommender import RecommenderAI
import json

userDataFilePath = './userDataFile.pickle'

class User(object):
    def __init__(self):
        self.name = "Junwon"
        self.email = "t-jupark@microsoft.com"
        self.role = "Software Engineering"
        self.team = "MSN"
        self.position = "Intern"
        self.managerName = "Somesh Goel"
        self.managerEmail = "sgoel@microsoft.com"
        self.thingsToTeach = []
        self.thingsTaught = []
        self.recommendedThingsToTeach = []
        self.chapter = 0
        self.saveUserData()
        self.lastUnansweredQuestion = ""
        self.faq = {}
        self.recommender = RecommenderAI(self.email)
        self.addThingsToTeach()
        self.updateRecommended()

    def addThingsToTeach(self): 
        file = json.loads(open('sample-journey.json').read())
        journey = file['journey']
        positionDocs = journey['position'].get(self.position.lower(), {"docs": []})["docs"]
        roleDocs = journey['role'].get(self.role.lower(), {"docs": []})["docs"]
        teamDocs = journey['team'].get(self.team.lower(), {"docs": []})["docs"]
        self.thingsToTeach = positionDocs + roleDocs + teamDocs

    def updateRecommended(self):
        recommended = set(self.recommender.user_recommendations()) - set(self.thingsTaught)
        self.recommendedThingsToTeach = list(recommended)


    def initUserData(self):
        with open(userDataFilePath, 'wb') as userDataFile:
            pickle.dump(self, userDataFile, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def loadUserData():
        if os.path.isfile(userDataFilePath):
            with open(userDataFilePath, 'rb') as userDataFile:
                self = pickle.load(userDataFile)
                return self
        else:
            return User()

    @staticmethod
    def removeUserData():
        os.remove(userDataFilePath)


    def saveUserData(self):
        with open(userDataFilePath, 'wb') as userDataFile:
            pickle.dump(self, userDataFile, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def extract_name(message):
        name = []
        name = re.findall('.*is\s(\w+).*', message.lower())
        if not name:
            name = re.findall('.*im\s(\w+).*', message.lower())
        if not name:
            name = re.findall('.*\'m\s(\w+).*', message.lower())
        if not name:
            name = re.findall('.*am\s(\w+).*', message.lower())
        if not name:
            name = re.findall('.*call\sme\s(\w+).*', message.lower())
        if not name:
            name = re.findall('.*known\sas\s(\w+).*', message.lower())
        if not name:
            name = re.findall('.*\'s\s(\w+).*', message.lower())
        if not name and len(message.split()) == 1:
            return message.title()
        if name:
            return name[0].title()
        else:
            return []
