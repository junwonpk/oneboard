#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from user import User
import re

user = User.loadUserData()
lastChapter = 7

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
    # body text is message.body["text"]
    user.chapter += 1
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

def chapter1(message):
    message.reply("Let’s get you ramped up on Microsoft One Engineering System (1ES).")
    message.reply("Go read this document: [link], and let me know once you have done this.")

def chapter2(message):
    message.reply("What do you not understand?")

def chapter3(message):
    message.reply("One way is to clone it to your local machine. Another way is to read it from Visual Studio Team")

def chapter4(message):
    message.reply("Awesome! Now, let's get relevant repositories on your local machine. Your org chart says you are in the Intune Team. You will probably need Intune-UX and Intune-Services. Please confirm with your manager that this is correct")

def chapter5(message):
    message.reply("Wonderful. So you need Intune-UX, Intune-Services, and Intune-SUPER-SECRET-REPOSITORIES")

def chapter6(message):
    message.reply("Please consult the following document for installing Intune-UX. Please let me know once you have finished")

def chapter7(message):
    message.reply("Based on previous experience with other employees, there’s an 80% that your error may be caused by the following")
