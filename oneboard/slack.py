from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re

from oneboard import Oneboard
from responseAI import ResponseAI

print "loading responseAI"
responseAI =  ResponseAI()
print "loaded responseAI"

@respond_to('sudo reset')
def reset(message):
    oneboard = Oneboard()
    oneboard.reset()
    message.reply('I forgot everything!')

@respond_to('.*')
def processMessage(message):
    oneboard = Oneboard()
    oneboard.processMessage(message, responseAI)

# @respond_to('My name is (.*)')
# def learnName(message, name):
#     user = loadUser()
#     user.name = name
#     user.saveUserData()
#     message.reply("Hello, " + user.name)
