from gensim.models import Word2Vec
import numpy as np
import scipy
import re

class ResponseAI(object):

    def __init__(self):
        self.model = self.loadGloveModel("./data/glove.42B.300d.txt")
        self.freq_dict = self.build_frequency_dictionary()
        self.faq_vectors = [] #This is a list of SENTENCE VECTORS
        self.DICT_CONSTANT = len(self.freq_dict)
        self.yes_answers = self.clean_sentence(["got it", "awesome", "cool", "amazing", "nice", "yes", "go", "go on", "continue", "got it", "sure", "move", "move on", "ready", "onward", "done", "got it", "next"])
        self.no_answers = self.clean_sentence(["huh", "why", "what", "when", "where", "wait", "confused", "question", "show", "possible", "sorry", "stop", "no"])
        self.yes_vectors = np.array([self.sentence2vec(ans) for ans in self.yes_answers])
        self.no_vectors = np.array([self.sentence2vec(ans) for ans in self.no_answers])
        self.set_base_faq_sentencevecs()

    # solve glove model loading time
    def loadGloveModel(self, gloveFile):
        f = open(gloveFile,'r')
        model = {}
        count = 0
        for line in f:
            count += 1
            splitLine = line.split()
            word = splitLine[0]
            embedding = np.array([float(val) for val in splitLine[1:]])
            model[word] = embedding
            if (count % 1000000) == 0: print count
        return model

    def clean_sentence(self, docs):
        stoplist = set('for a of the and to in'.split())
        text = [[word for word in document.lower().split() if word not in stoplist]
            for document in docs]
        return text

    def build_frequency_dictionary(self):
        word_frequency_data = [line.rstrip('\n') for line in open('./data/20k.txt')]
        word_frequency_data = {k: v for v, k in enumerate(word_frequency_data)}
        #print(type(word_frequency_data))
        return word_frequency_data

    def set_base_faq_sentencevecs(self):
        lines = [line.rstrip('\n') for line in open('./data/faq.txt')]
        for line in lines:
            line = self.clean_line(line)
            self.faq_vectors.append(self.get_sentencevec(line))

    def clean_line(self, line_to_clean):
        print(line_to_clean)
        common_words = [line.rstrip('\n').lower() for line in open('./data/common-50.txt')]
        line_to_clean = re.sub('[^a-zA-Z ]', '', line_to_clean)
        line_to_clean = [word for word in line_to_clean.lower().split()]
        cleaned_line = []
        for word in line_to_clean:
            if word not in common_words:
                cleaned_line.append(word)
        return cleaned_line

    def get_weight(self, word):
        try:
            return self.DICT_CONSTANT - self.freq_dict[word] #The idea is to reverse the indexing so less common words = more important.
        except:
            return self.DICT_CONSTANT

    def get_sentencevec(self, line):
        #Sentence vector is sum of (wordvec for each word)*(1/1+f), where f is frequency.
        sentence_vec = []
        for word in line:
            multiplier = (float(1e7)/float(1+self.get_weight(word)))
            wordvec = np.array([self.word_to_vec(word)])
            weighted_wordvec = multiplier*wordvec
            sentence_vec.append(weighted_wordvec)
        sentence_vec = np.sum(sentence_vec, axis=0)
        sentence_vec /= float(len(line))
        return sentence_vec

    def word_to_vec(self, word):
        wordvec_list = []
        # word = filter(str.isalpha, word)
        try:
            wordvec = self.model[word] # e.g. wordvec["emily"] = [3,5,524,234]
            wordvec_list.append(wordvec)
        except:
            pass
        if not wordvec_list:
            return np.zeros(300)
        data = np.array(wordvec_list)
        vec = data.mean(axis=0)
        return vec

    def find_shortest(self, question_sentencevec):
        min_values = []
        for i in range(len(self.faq_vectors)):
            min_values.append(scipy.spatial.distance.euclidean(question_sentencevec, self.faq_vectors[i]))
        return np.argmin(min_values), np.min(min_values)

    # message is an array
    def sentence2vec(self, message):
        wordvec_list = []
        for word in message:
            # word = filter(str.isalpha, word)
            try:
                wordvec = self.model[word] # e.g. wordvec["emily"] = [3,5,524,234]
                wordvec_list.append(wordvec)
            except:
                pass
        if not wordvec_list:
            return np.zeros(300)

        data = np.array(wordvec_list)
        vec = data.mean(axis=0)
        return vec

    def decide_question(self, question):
        question = self.clean_line(question)
        question_sentencevec = self.get_sentencevec(question)
        result, confident = self.find_shortest(question_sentencevec)

    def intentClassifier(self, message):
        message_vec = self.sentence2vec(message.split(' '))

        no_dots = self.no_vectors.dot(message_vec)
        max_no = no_dots.max()

        yes_dots = self.yes_vectors.dot(message_vec)
        max_yes = yes_dots.max()

        return max_yes > max_no