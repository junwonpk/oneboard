from gensim.models import Word2Vec
import numpy as np
import scipy
import re

class responseAI(object):

    def __init__(self):
        self.model = loadGloveModel("../data/glove.42B.300d.txt")
        self.lastChapter = 7

    def loadGloveModel(gloveFile):
        print "Loading Glove Model"
        f = open(gloveFile,'r')
        model = {}
        for line in f:
            splitLine = line.split()
            word = splitLine[0]
            embedding = np.array([float(val) for val in splitLine[1:]])
            model[word] = embedding
        return model


    def clean_sentence(docs):
        stoplist = set('for a of the and to in'.split())
        text = [[word for word in document.lower().split() if word not in stoplist]
            for document in docs]
        return text

    def build_frequency_dictionary():
        word_frequency_data = [line.rstrip('\n') for line in open('./20k.txt')]
        word_frequency_data = {k: v for v, k in enumerate(word_frequency_data)}
        #print(type(word_frequency_data))
        return word_frequency_data

    freq_dict = build_frequency_dictionary()
    #print(len(freq_dict))


    faq_vectors = [] #This is a list of SENTENCE VECTORS
    DICT_CONSTANT = len(freq_dict)

    def set_base_faq_sentencevecs():
        lines = [line.rstrip('\n') for line in open('./faq.txt')]
        for line in lines:
            line = clean_line(line)
            faq_vectors.append(get_sentencevec(line))

    def clean_line(line_to_clean):
        print(line_to_clean)
        common_words = [line.rstrip('\n').lower() for line in open('./common-50.txt')]
        line_to_clean = re.sub('[^a-zA-Z ]', '', line_to_clean)
        line_to_clean = [word for word in line_to_clean.lower().split()]
        cleaned_line = []
        for word in line_to_clean:
            if word not in common_words:
                cleaned_line.append(word)
        return cleaned_line

    def get_weight(word):
        try:
            return DICT_CONSTANT-freq_dict[word] #The idea is to reverse the indexing so less common words = more important.
        except:
            return DICT_CONSTANT

    def get_sentencevec(line):
        #Sentence vector is sum of (wordvec for each word)*(1/1+f), where f is frequency.
        sentence_vec = []
        for word in line:
            multiplier = (float(1e7)/float(1+get_weight(word)))
            wordvec = np.array([word_to_vec(word)])
            weighted_wordvec = multiplier*wordvec
            sentence_vec.append(weighted_wordvec)
        sentence_vec = np.sum(sentence_vec, axis=0)
        sentence_vec /= float(len(line))
        return sentence_vec

    def word_to_vec(word):
        wordvec_list = []
        word = filter(str.isalpha, word)
        try:
            wordvec = model[word] # e.g. wordvec["emily"] = [3,5,524,234]
            wordvec_list.append(wordvec)
        except:
            pass
        if not wordvec_list:
            return np.zeros(300)

        data = np.array(wordvec_list)
        vec = data.mean(axis=0)
        return vec

    set_base_faq_sentencevecs()

    def find_shortest(question_sentencevec):
        min_values = []
        for i in range(len(faq_vectors)):
            min_values.append(scipy.spatial.distance.euclidean(question_sentencevec, faq_vectors[i]))
        return np.argmin(min_values)

    def init():
        build_frequency_dictionary()
        set_base_faq_sentencevecs()

    @staticmethod
    def decide_question(question):
        question = clean_line(question)
        question_sentencevec = get_sentencevec(question)

        #Then find the shortest one between the sentencevec of user question and sentencevec of faq's
        result = find_shortest(question_sentencevec)
        print(result)

    decide_question("What should I know about pull requests?")

    yes_answers = ["got it", "awesome", "cool", "amazing", "nice", "yes", "go", "go on", "continue", "got it", "sure", "move", "move on", "ready", "onward", "done", "got it", "next"]
    no_answers = ["huh", "why", "what", "when", "where", "wait", "confused", "question", "show", "possible", "sorry", "stop", "no"]

    yes_answers = clean_sentence(yes_answers)
    no_answers = clean_sentence(no_answers)

    # message is an array
    def sentence2vec(message):
        wordvec_list = []
        for word in message:
            word = filter(str.isalpha, word)
            try:
                wordvec = model[word] # e.g. wordvec["emily"] = [3,5,524,234]
                wordvec_list.append(wordvec)
            except:
                pass
        if not wordvec_list:
            return np.zeros(300)

        data = np.array(wordvec_list)
        vec = data.mean(axis=0)
        return vec

    yes_vectors = np.array([sentence2vec(ans) for ans in yes_answers])
    print (yes_vectors)
    no_vectors = np.array([sentence2vec(ans) for ans in no_answers])

    def intentClassifier(message):
        message_vec = sentence2vec(message.split(' '))

        no_dots = no_vectors.dot(message_vec)
        #print("no dots:")
        #print(no_dots)
        max_no = no_dots.max()

        yes_dots = yes_vectors.dot(message_vec)
        max_yes = yes_dots.max()
        #print("yes dots:")
        #print(yes_dots)

        #print(max_yes)
        #print(max_no)
        print (max_yes > max_no)
        return max_yes > max_no

        #print(intent)
        #return intent

    intentClassifier('Sure. I\'m ready to move on.')
    intentClassifier('Go ahead')
    intentClassifier('next resource please')
    intentClassifier('done')
    intentClassifier('cool. i get it.')
    intentClassifier('Cool. I get it.')
    intentClassifier('no...')
    intentClassifier('I have a question. What is Ibiza?')
    intentClassifier('Is it possible for you to show me resources regarding Azure Active Directory?')
    intentClassifier('Sure. What\'s next?')
