#!/usr/bin/env python
# -*- coding: utf-8 -*-

from user import User
from responseAI import ResponseAI
from database import Database
import re

class Oneboard(object):
    def __init__(self):
        self.user = User.loadUserData()
        self.lastChapter = 4
        self.database = Database()

    def reset(self):
        self.user.removeUserData()

    def saveNewFAQAnswer(self, answerToQuestion):
        self.user.faq[self.user.lastUnansweredQuestion] = answerToQuestion
        self.user.lastUnansweredQuestion = ""

    def UserSaysGoOn(self, message, responseAI): # return true if go on, false if stay
        return responseAI.intentClassifier(message.body["text"])

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

    def CanFindInFAQ(self, message, responseAI):
        faq_index, distance = responseAI.decide_question(message.body["text"])
        return distance < self.database.faqMaxDistance

    def GetFAQSolution(self, message, responseAI):
        faq_index, distance = responseAI.decide_question(message.body["text"])
        return self.database.faq.keys()[faq_index]

    def incrementState(self):
        self.user.chapter += 1
        self.user.chapter = (self.user.chapter%4)
        self.user.saveUserData()

    def decrementState(self):
        self.user.chapter -= 1
        self.user.chapter = (self.user.chapter%4)
        self.user.saveUserData()

    # def getStaticResource(self, topic):
    #     static_info =  {'1ES':'aka.ms/1ES','Intune':'aka.ms/Intune','Ibiza':'aka.ms/Ibiza'}
    #     return static_info[topic]

    ####Documentation for the four chapters####
    # Chapter 0: Gives the user the next thing that they'll go over
    # Chapter 1: Either gives next thing to go over or provides help
    # Chapter 2: Gets user to answer question
    # Chapter 3: Saves user answer and moves on

    def processMessage(self, message, responseAI):
        # chapters = self.loadChapters()
        # chapter = chapters[self.user.chapter]
        # chapter(message)

        # ##body text is message.body["text"]
        if(self.user.chapter == 0):
            file = json.loads(open('./oneboard/sample-journey.json').read()) 
            docs = file['docs'] 
            if (self.user.thingsToTeach):
                nextItemID = self.user.thingsToTeach.pop()
                next = docs.get(nextItemName, {"name": nextItemID, "link": "aka.ms/msw"})
                self.user.thingsTaught.append(nextItemID)

                if(self.user.isNew):
                    message.reply("Welcome, " + self.user.name + "! So excited to have you at Microsoft. Let's get you onboarded!")
                    message.reply("The first thing that we'll go over is " + next['name'] + ".")
                    self.user.isNew = False
                else:
                    message.reply("The next thing that we'll go over is " + next['name'] + ".")

                message.reply("Take a look at ' + next['link'] + ' and let me know when you are ready to move on.")
                message.reply("If you aren't, ask me any question you have!")
                self.incrementState()
            else:
                message.reply("Awesome! Looks like you finished the onboarding process!")
        elif(self.user.chapter == 1):
            if(self.UserSaysGoOn(message, responseAI)):
                next = self.user.thingsToTeach.pop()
                # TODO: save in things taught.
                thingsTaught.append(next)
                message.reply("The next thing that we'll go over is " + next + ".")
                # resource = self.getStaticResource(next)
                message.reply("Please learn the term on MSW and let me know when you are ready to move on.")
                message.reply("If you aren't, ask me any question you have!")
            else:
                self.incrementState()
                message.reply("Ah. Let me see if I can help...")
                # TODO: special guard. if we tried FAQ once, and returned here, force move to new FAQ
                if (self.CanFindInFAQ(message, responseAI)):
                    solution = self.GetFAQSolution(message, responseAI)
                    message.reply("Can you try the following: LINK TO QUESTION " + solution + " and tell me if it works?")
                    #Stay in state here because if user says go on, you'll give them something to go over.
                else:
                    message.reply("I'm sorry, I don't know the answer to this question. Please consult your manager and teach me the info.")
                    message.reply("When you are ready, please type in the question you asked.")
                    self.incrementState()
        elif(self.user.chapter == 2):
            self.user.lastUnansweredQuestion = message.body["text"]
            message.reply("Got it. And what was the answer?")
            self.incrementState()
        elif(self.user.chapter == 3):
            self.saveNewFAQAnswer(message.body["text"])
            message.reply("Got it. Now I learnt something new!")
            message.reply("Should we move on to the next topic?")
            self.decrementState()
            self.decrementState()

    def loadChapters(self):
        chapters = {}
        for chapter in xrange(self.lastChapter + 1):
            chapters[chapter] = eval('self.chapter' + str(chapter))
        return chapters

    # def chapter0(self, message):
    #     message.reply("Nice to meet you, {}! Welcome to Microsoft!".format(self.user.name))
    #     message.reply("I'm Oneboard, and I'll be guiding you through Microsoft resources until you feel fully onboarded!")
    #     message.reply("It seems like you are {} in {}. Does this sound right?".format(self.user.role,self.user.team))
    #
    # def chapter1(self, message):
    #     message.reply("Let’s get you ramped up on Microsoft One Engineering System (1ES).")
    #     message.reply("Go read this document: [link], and let me know once you have done this.")
    #
    # def chapter2(self, message):
    #     message.reply("What do you not understand?")
    #
    # def chapter3(self, message):
    #     message.reply("One way is to clone it to your local machine. Another way is to read it from Visual Studio Team")
    #
    # def chapter4(self, message):
    #     message.reply("Awesome! Now, let's get relevant repositories on your local machine. Your org chart says you are in the Intune Team. You will probably need Intune-UX and Intune-Services. Please confirm with your manager that this is correct")
    #
    # def chapter5(self, message):
    #     message.reply("Wonderful. So you need Intune-UX, Intune-Services, and Intune-SUPER-SECRET-REPOSITORIES")
    #
    # def chapter6(self, message):
    #     message.reply("Please consult the following document for installing Intune-UX. Please let me know once you have finished")
    #
    # def chapter7(self, message):
    #     message.reply("Based on previous experience with other employees, there’s an 80% that your error may be caused by the following")
