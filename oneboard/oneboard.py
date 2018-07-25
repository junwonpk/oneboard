from slackbot.bot import respond_to
from slackbot.bot import listen_to
import pickle
import re

userDataFilePath = './userDataFile.pickle'

@respond_to('oneboard', re.IGNORECASE)
def hi(message):
    message.reply('I am oneboard!')
    # react with thumb up emoji
    message.react('+1')

@respond_to('Give me (.*)')
def giveme(message, something):
    message.reply('Here is {}'.format(something))

@respond_to('.*')
def processMessage(message):
    message.reply('Processed.')

@respond_to('My name is (.*)')
def learnName(message, name):
    initUserData()
    userData = getUserData()
    userData["name"] = name
    setUserData(userData)
    message.reply("Hello, " + userData["name"])

def initUserData():
    userData = {"name": "unknown"}
    with open(userDataFilePath, 'wb') as userDataFile:
        pickle.dump(userData, userDataFile, protocol=pickle.HIGHEST_PROTOCOL)

def getUserData():
    with open(userDataFilePath, 'rb') as userDataFile:
        return pickle.load(userDataFile)

def setUserData(userData):
    with open(userDataFilePath, 'wb') as userDataFile:
        pickle.dump(userData, userDataFile, protocol=pickle.HIGHEST_PROTOCOL)
