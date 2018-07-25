from slackbot.bot import respond_to
from slackbot.bot import listen_to
from user import User
import re

user = User.loadUserData()
lastChapter = 2

def loadChapters():
    chapters = {}
    for chapter in xrange(lastChapter + 1):
        chapters[chapter] = eval('chapter' + str(chapter))
    return chapters

@respond_to('sudo reset')
def reset(message):
    User.removeUserData()
    message.reply('I forgot everything!')

@respond_to('.*')
def processMessage(message):
    chapters = loadChapters()
    chapter = chapters[user.chapter]
    chapter(message)
    user.saveUserData

# @respond_to('My name is (.*)')
# def learnName(message, name):
#     user = loadUser()
#     user.name = name
#     user.saveUserData()
#     message.reply("Hello, " + user.name)

def chapter0(message):
    message.reply("Nice to meet you, {}! Welcome to Microsoft!".format(user.name))
    message.reply("I'm Oneboard, and I'll be guiding you through Microsoft resources until you feel fully onboarded!")
    message.reply("It seems like you are {} in {}. Does this sound right?".format(user.role,user.team))
    user.chapter += 1

def chapter1(message):
    message.reply("Great! Tell me your name.")
    user.chapter += 1

def chapter2(message):
    print(message)
    print(message.body["text"])
    user.name = extract_name(message.body["text"])
    message.reply("Your name is {}".format(user.name))

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
