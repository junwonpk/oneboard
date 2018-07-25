from slackbot.bot import respond_to
from slackbot.bot import listen_to
from user import User
import re

def loadUser():
    return User.loadUserData()

@respond_to('sudo reset')
def reset(message):
    User.removeUserData()
    message.reply('I forgot everything!')

@respond_to('.*')
def processMessage(message):
    user = loadUser()
    message.reply('Your name is ' + user.name)

@respond_to('My name is (.*)')
def learnName(message, name):
    user = loadUser()
    user.name = name
    user.saveUserData()
    message.reply("Hello, " + user.name)
