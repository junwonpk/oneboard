import os
import pickle

userDataFilePath = './userDataFile.pickle'

class User(object):
    def __init__(self):
        self.name = "unknown"
        self.email = "unknown@microsoft.com"
        self.role = "Software Engineering Intern"
        self.team = "Intune Data Team"
        self.managerName = "Somesh Goel"
        self.managerEmail = "sgoel@microsoft.com"
        self.thingsToTeach = ["Intune", "Ibiza", "1ES"]
        self.thingsTaught = ["Benefits", "Signature Event"]
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
