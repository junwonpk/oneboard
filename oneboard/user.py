import os
import pickle

userDataFilePath = './userDataFile.pickle'

class User(object):
    def __init__(self):
        self.name = "Junwon"
        self.email = "t-jupark@microsoft.com"
        self.role = "A Software Engineering Intern"
        self.team = "Intune Data Team"
        self.managerName = "Somesh Goel"
        self.managerEmail = "sgoel@microsoft.com"
        self.thingsToTeach = ["1ES", "Intune", "Ibiza"]
        self.thingsTaught = ["Benefits", "Signature Event"]
        self.chapter = 0
        self.saveUserData()

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
