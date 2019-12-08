from collections import Counter
import collections 
import re
import random
import math

class Ngram_Language_Model:
    """The class implements a Markov Language Model that learns amodel from a given text.
        It supoprts language generation and the evaluation of a given string.
        The class can be applied on both word level and caracter level.
    """

    def __init__(self, n=3, chars=False):
        """Initializing a language model object.
        Arges:
            n (int): the length of the markov unit (the n of the n-gram). Defaults to 3.
            chars (bool): True iff the model consists of ngrams of characters rather then word tokens.
                          Defaults to False
        """ 
        self.n = n
        self.chars = chars
        self.ngrams_dictionaries = {}

    def build_model(self, text):  #should be called build_model
        """populates a dictionary counting all ngrams in the specified text.

            Args:
                text (str): the text to construct the model from.
        """
        # Loop through all lines and words and add n-grams to dict
        tokens = [token for token in text.split(" ") if token != ""]
        self.text = text
        for j in range(1,self.n+1):
            # Use the zip function to help us generate n-grams
            # Concatentate the tokens into ngrams and return
            ngrams_dictionary = []
            ngrams = zip(*[tokens[i:] for i in range(j)])
            ngrams = (' '.join(ngram) for ngram in ngrams)
            ngrams_count = collections.defaultdict(int)
            for ngram in ngrams:
                ngrams_count[ngram] += 1
            ngrams_dictionary = ngrams_count
            self.ngrams_dictionaries[j] = ngrams_dictionary
        
    def get_model(self):
        """Returns the model as a dictionary of the form {ngram:count}
        """
        return self.ngrams_dictionaries[self.n]

    def generate(self, context=None, n=20):
        """Returns a string of the specified length, generated by applying the language model
        to the specified seed context. If no context is specified the context should be sampled
        from the models' contexts distribution. Generation should stop before the n'th word if the
        contexts are exhausted.

            Args:
                context (str): a seed context to start the generated string from. Defaults to None
                n (int): the length of the string to be generated.

            Return:
                String. The generated text.

        """
        current_ngram, full_output_sentence = [], []
        
        if(context is None):
            #print("Choosing random n-gram = {}".format(current_ngram))
            current_ngram = random.choice(list(self.ngrams_dictionaries[self.n].keys()))
        else:    
            current_ngram = context
     
        current_ngram_length = len(current_ngram.split(' '))
        potential_ngrams = []
        i = 0
        full_output_sentence.append(current_ngram)
        
        if(current_ngram_length < self.n-1):
            #print("context given was size of = {}".format(current_ngram_length))
            for s in range(current_ngram_length+1,self.n):
                #iterating over the language, looking for all possibles ngrams to complete
                for key, value in self.ngrams_dictionaries[s].items():
                    if(isinstance(key, str) and key.startswith(current_ngram)):
                        #print("n-gram {} can potentially complete our sentence!".format(key))
                        for l in range(1,value+1):
                            potential_ngrams.append(key)                        
                        #print("Potential ngrams = {}".format(potential_ngrams))
                    #else:
                        #print("n-gram {} can NOT complete our sentence!".format(key))
            #print("Potential ngrams = {}".format(potential_ngrams))
            if not potential_ngrams:
                return ' '.join(full_output_sentence)
            else: 
                chosen_ngram = ' '.join(random.choices(potential_ngrams))            
                #print("Appending the completed ngram that was found to our sentence = {}".format(chosen_ngram))
                full_output_sentence.append(chosen_ngram.split(' ')[-1])
                #print("Full Sentence Output now is = {}".format(full_output_sentence))
                current_ngram = chosen_ngram
            
        i = current_ngram_length
        #print("Full Sentence Output = {}".format(full_output_sentence))
            
        #iterate until we get to n words total
        while i < n-1:
            #print("We have {} words count so far, can still add more words to our sentence".format(i))
            #calculating the new gram to be completed
            current_ngram = current_ngram.split(' ')
            current_ngram.reverse()
            new_ngram_to_complete = []
            for a in range(0,self.n-1):
                new_ngram_to_complete.append(current_ngram[a])

            new_ngram_to_complete.reverse()
            new_ngram_to_complete_string = ' '.join(new_ngram_to_complete)
            #print("New ngram to complete now is = {}".format(new_ngram_to_complete_string))
            potential_ngrams = []

            #iterating over the language, looking for all possibles ngrams to complete
            for key, value in self.ngrams_dictionaries[self.n].items():
                if(isinstance(key, str) and key.startswith(new_ngram_to_complete_string)):
                    #print("n-gram {} can potentially complete our sentence!".format(key))
                    for l in range(1,value+1):
                        potential_ngrams.append(key)                        
                    #print("Potential ngrams = {}".format(potential_ngrams))
                #else:
                    #print("n-gram {} can NOT complete our sentence!".format(key))
            #print("Potential ngrams = {}".format(potential_ngrams))
            if not potential_ngrams:
                return ' '.join(full_output_sentence)
            else: 
                chosen_ngram = ' '.join(random.choices(potential_ngrams))            
                #print("Appending the completed ngram that was found to our sentence = {}".format(chosen_ngram))
                full_output_sentence.append(chosen_ngram.split(' ')[-1])
                #print("Full Sentence Output now is = {}".format(full_output_sentence))
                i = i + 1
                current_ngram = chosen_ngram
        return ' '.join(full_output_sentence)
            
            
    def evaluate(self,text):
        """Returns the log-likelihod of the specified text to be generated by the model.
           Laplace smoothing should be applied if necessary.

           Args:
               text (str): Text to ebaluate.

           Returns:
               Float. The float should reflect the (log) probability.
        """
        #print("Evaluating: {}".format(text))
        sum_likelihood = 0.0
        split_text = text.split()
        for index in range(len(split_text)):
            count_seq = 0
            count_prefix = 0
            #print("index = {}, split_text = {}".format(index,split_text))
            given_text = normalize_text(text)
            #print("normalize text = {}".format(given_text))
            if index - (self.n - 1) < 0:
                #print("flow 1")
                prefix = ' '.join([x for x in split_text[0:index]])
                suffix = split_text[index]
                #print("prefix = {}".format(prefix))
                #print("suffix = {}".format(suffix))
                if not self.chars:
                    seq = prefix + ' ' + suffix
                else:
                    seq = prefix + suffix
                if index == 0:
                    #print("flow 1->2")
                    seq = seq.replace(' ', '')
                    #print("seq = {}".format(seq))
                    for key, value in self.ngrams_dictionaries[self.n].items():
                        if key.startswith(seq):
                            count_seq = count_seq + value
                    count_prefix = count_prefix + len(self.text.split()) - self.n + 1
                else:
                    #print("flow 1->3")
                    #print("seq = {}".format(seq))
                    #print("count_seq = {}".format(count_seq))
                    for key, value in self.ngrams_dictionaries[self.n].items():
                            if key.startswith(seq):
                                count_seq = count_seq + value
                                #print("count_seq = {}".format(count_seq))
                                #print("key = {} STARTS!!! with = {}".format(key,seq))
                            #else:
                                #print("key = {} doesn't start with = {}".format(key,seq))
                    count_prefix = self._count_check_anagram(prefix)
                    #print("count_prefix = {}".format(count_prefix))
                    #print("count_seq = {}".format(count_seq))
                if count_seq == 0:
                    #print("seq = {}, smoothing!".format(seq))
                    return math.log(self.smooth(seq))
            else:
                #print("flow 2")
                prefix = split_text[(index - self.n + 1): index]
                suffix = split_text[index]
                #print("prefix = {}".format(prefix))
                #print("suffix = {}".format(suffix))
                if self.chars:
                    seq = (''.join([x for x in prefix])) + suffix
                else:
                    seq = (' '.join([x for x in prefix])) + ' ' + suffix
                if seq not in self.ngrams_dictionaries[self.n].keys():
                    #print("seq = {}, smoothing!".format(seq))
                    return math.log(self.smooth(seq))
                count_seq = 0
                for key, value in self.ngrams_dictionaries[self.n].items():
                        if key.startswith(seq):
                            count_seq = count_seq + value
                        #else:
                            #print("key = {} doesn't start with = {}".format(key,seq))
                count_prefix = 0
                for key, value in self.ngrams_dictionaries[self.n].items() or count_seq == 0:
                        if key.startswith(' '.join(prefix)):
                            count_prefix = count_prefix + value
                #print("count_prefix = {}".format(count_prefix))
                #print("count_seq = {}".format(count_seq))
            sum_likelihood += math.log((count_seq / count_prefix))   
            #print("------------")
        #print("sum of likelihood = {}".format(sum_likelihood))
        return sum_likelihood

    def _count_check_anagram(self, prefix):
        """count how many the given prefix is part of the vocabulary of our model.
                   Args:
                       prefix (string): the prefix of the key
                   Returns:
                       the count of occuraences of the given prefix in the vocabulary of the model.
        """
        counter = 0
        dict = self.ngrams_dictionaries[self.n]
        for key, value in self.ngrams_dictionaries[self.n].items():
            if key.startswith(prefix):
                counter += value
        return counter
      
    def smooth(self, ngram):
        """Returns the smoothed (Laplace) probability of the specified ngram.

            Args:
                ngram (str): the ngram to have it's probability smoothed

            Returns:
                float. The smoothed probability.
        """
        ngram_count = self.ngrams_dictionaries[self.n][ngram]
       
        if(ngram_count == 0):
            del self.ngrams_dictionaries[self.n][ngram]
            
        total_ngram_count = len(self.ngrams_dictionaries[self.n].keys())     
        vocabulary_count = len(set(self.text.split()))
        return (ngram_count + 1) / (total_ngram_count + vocabulary_count)

def normalize_text(text):
    """Returns a normalized string based on the specifiy string.
       You can add default parameters as you like (they should have default values!)
       You should explain your decitions in the header of the function.

       Args:
           text (str): the text to normalize

       Returns:
           string. the normalized text.
    """
    text = re.sub('([.,!?()])', r' \1 ', text)
    text = re.sub('\s{2,}', ' ', text)
    text = text.replace('\n', ' ').replace('\r', '')
    return text.lower()

def stripNonAlphaNum(text):
    import re
    return re.compile(r'\W+', re.UNICODE).split(text)

def who_am_i():
    """Returns a ductionary with your name, id number and email. keys=['name', 'id','email']
        Make sure you return your own info!
    """
    return {'name': 'Tal Yitzhak', 'id': '204260533', 'email': 'talyitzhak100@gmail.com'}
