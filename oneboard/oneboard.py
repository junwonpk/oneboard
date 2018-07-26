#!/usr/bin/env python
# -*- coding: utf-8 -*-

from user import User
from responseAI import ResponseAI
import re

class Oneboard(object):
    def __init__(self):
        self.user = User.loadUserData()
        self.lastChapter = 7

    def reset(self):
        self.user.removeUserData()

    def processMessage(self, message, responseAI):
        print "message received"
        if responseAI.intentClassifier(message.body["text"]):
            message.reply("intent classifier says: true")
        else:
            message.reply("intent classifier says: false")


        faq, conf = responseAI.decide_question(message.body["text"])
        message.reply("faq classifier says: {} with {} confidence".format(faq, conf))

        # chapters = self.loadChapters()
        # chapter = chapters[self.user.chapter]
        # chapter(message)
        # # body text is message.body["text"]
        # self.user.chapter += 1
        # self.user.saveUserData()

    def loadChapters(self):
        chapters = {}
        for chapter in xrange(self.lastChapter + 1):
            chapters[chapter] = eval('self.chapter' + str(chapter))
        return chapters

    def chapter0(self, message):
        message.reply("Nice to meet you, {}! Welcome to Microsoft!".format(self.user.name))
        message.reply("I'm Oneboard, and I'll be guiding you through Microsoft resources until you feel fully onboarded!")
        message.reply("It seems like you are {} in {}. Does this sound right?".format(self.user.role,self.user.team))

    def chapter1(self, message):
        message.reply("Let’s get you ramped up on Microsoft One Engineering System (1ES).")
        message.reply("Go read this document: [link], and let me know once you have done this.")

    def chapter2(self, message):
        message.reply("What do you not understand?")

    def chapter3(self, message):
        message.reply("One way is to clone it to your local machine. Another way is to read it from Visual Studio Team")

    def chapter4(self, message):
        message.reply("Awesome! Now, let's get relevant repositories on your local machine. Your org chart says you are in the Intune Team. You will probably need Intune-UX and Intune-Services. Please confirm with your manager that this is correct")

    def chapter5(self, message):
        message.reply("Wonderful. So you need Intune-UX, Intune-Services, and Intune-SUPER-SECRET-REPOSITORIES")

    def chapter6(self, message):
        message.reply("Please consult the following document for installing Intune-UX. Please let me know once you have finished")

    def chapter7(self, message):
        message.reply("Based on previous experience with other employees, there’s an 80% that your error may be caused by the following")
