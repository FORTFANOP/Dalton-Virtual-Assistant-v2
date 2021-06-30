import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import pickle
import json
from tensorflow.keras.models import load_model
from tensorflow.python.util import deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)


class DaltonAI:
    def __init__(self, model_path):
        self.model_path = model_path
        pass

    def clean_up_sentence(self, sentence):
        # import nltk
        # from nltk.stem import WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()
        # tokenize the pattern - split words into array
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word - create short form for word
        sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
    def bow(self, sentence, words, show_details=True):
        # import numpy as np
        # import warnings
        # warnings.simplefilter(action='ignore', category=FutureWarning)
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0] * len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print("Found in bag: %s" % w)
        return np.array(bag)

    def predict_class(self, sentence, model):
        words = pickle.load(open('words.pkl', 'rb'))
        classes = pickle.load(open('classes.pkl', 'rb'))
        # filter out predictions below a threshold
        p = self.bow(sentence, words, show_details=False)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        return return_list

    def getResponse(self, ints, intents_json):
        import random
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result

    def chatbot_response(self, msg):
        """
        Outputs a response from the model.
        Pass in the input text to receive a response from the model.
        Parameters:
        msg --> The required input text
        """
        model = load_model(self.model_path)
        intents = json.loads(open('intents.json').read())
        ints = self.predict_class(msg, model)
        res = self.getResponse(ints, intents)
        return res

    # response_from_bot = chatbot_response(input_query)
