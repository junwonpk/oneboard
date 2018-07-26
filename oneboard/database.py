import os
import pickle

dbDataFilePath = './dbDataFile.pickle'

class Database(object):
    def __init__(self):
        self.company = "Microsoft"
        self.faq = {
            "How can I find out about my corporate benefits?": "answer1",
            "I have a problem with Visual Studio.": "answer2",
            "How do I get connected to the internet (corpnet)?": "answer",
            "Where do I fill my timecard?": "answer",
            "How can I get authorization to view [this document]?": "answer",
            "How can I download or set up Teams?": "answer",
            "How do I join my team on Teams?": "answer",
            "How do I make a pull request?": "answer",
            "Where do I find lists of issues and known bugs?": "answer",
            "How does code review work?": "answer",
            "Where is documentation for [certain feature]?": "answer",
            "How do I write a Connect?": "answer"
        }
        self.saveDB()

    def initDB(self):
        with open(dbDataFilePath, 'wb') as dbDataFile:
            pickle.dump(self, dbDataFile, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def loadDB():
        if os.path.isfile(dbDataFilePath):
            with open(dbDataFilePath, 'rb') as dbDataFile:
                self = pickle.load(dbDataFile)
                return self
        else:
            return Database()

    @staticmethod
    def removeDB():
        os.remove(dbDataFilePath)

    def saveDB(self):
        with open(dbDataFilePath, 'wb') as dbDataFile:
            pickle.dump(self, dbDataFile, protocol=pickle.HIGHEST_PROTOCOL)
