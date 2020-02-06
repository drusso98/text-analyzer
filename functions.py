import nltk
nltk.download('wordnet')
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from nltk import FreqDist, pos_tag
import matplotlib.pyplot as plt
import math
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

# The CMU Pronouncing Dictionary provides a mapping orthographic/phonetic
# for English words in their North American pronunciations.
from nltk.corpus import cmudict


#tokenize text removing punctaction
def token(text):
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text)
    return words


#removing stopwords
def del_stopwords(text):
    stop_words = set(stopwords.words("english"))
    filtered_sent = []
    lower_text = text.lower()
    for w in token(lower_text):
        if w not in stop_words:
            filtered_sent.append(w)
    return filtered_sent


#reduncing inflected words to their word stem, base or root form
def stemming(text):
    ps = PorterStemmer()

    stemmed_words = []
    for w in del_stopwords(text):
        stemmed_words.append(ps.stem(w))
    # print(stemmed_words)
    return stemmed_words


def lemmas(text):
    lem = WordNetLemmatizer()

    stemmed_words = []
    for w in del_stopwords(text):
        stemmed_words.append(lem.lemmatize(w))
    # print(stemmed_words)
    return stemmed_words


#counters
def word_count(text):
    return len(token(text))


def sentence_count(text):
    sentences = sent_tokenize(text)
    return len(sentences)


def char_count_spaces(text):
    return len(text)


def char_count_nospace(text):
    return len(text) - text.count(' ')


def syllables(word):
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count += 1
    if count == 0:
        count += 1
    return count


def word_syllable_count(word):
    # cmudict lexicon as a dictionary, whose keys are lowercase words
    # and whose values are lists of pronunciations.
    d = cmudict.dict()
    try:
        return max([len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]])
    except KeyError:
        # if word not found in cmudict
        return syllables(word)


def text_syllable_count(text):
    words = token(text)
    count = 0
    for word in words:
        count += word_syllable_count(word)
    return count


# plot the distributions
def words_length_distribution(text):
    words = del_stopwords(text)
    plt.ion()
    fig = plt.figure(figsize=(10, 4))
    fig.suptitle("WORDS'S LENGTH DISTRIBUTION")
    plt.gcf().subplots_adjust(bottom=0.15)
    fdist = FreqDist(len(token) for token in words)
    fdist.plot(30, cumulative=False)
    fig.savefig('wldis.png', bbox_inches="tight")
    return fdist.most_common((10))


def words_distribution(text):
    words = lemmas(text)
    plt.ion()
    fig = plt.figure(figsize=(10, 4))
    fig.suptitle("WORDS DISTRIBUTION")
    plt.gcf().subplots_adjust(bottom=0.15)
    fdist = FreqDist(words)
    fdist.plot(30, cumulative=False)
    fig.savefig('wdis.png', bbox_inches="tight")
    return fdist.most_common((10))


#standard deviation
def arithmetic_mean(text):
    return char_count_nospace(text)/word_count(text)


def standard_dev(text):
    card = word_count(text)
    mean = arithmetic_mean(text)
    sum = 0
    for i in token(text):
        sum += (len(i) - mean)**2
    return math.sqrt(sum/card)


# part-of-speech tagging: process of marking up a word in a text (corpus)
# as corresponding to a particular part of speech
def pos_tagging(text):
    words = del_stopwords(text)
    return pos_tag(words)


# Lexical density estimates the linguistic complexity in a written or spoken composition
# from the functional words (grammatical units) and content words (lexical units, lexemes).
# # take out to be, have, do
def lexical_density(text):
    tags = pos_tagging(text)
    all_tags = {tag: [t for t in tags if t[1] == tag] for tag in ["JJ","JJR","JJS","NN","NNS","NNP","NNPS","RB","RBR","RBS", "VB", "VBN", "VBP", "VBZ", "VBG", "VBD"]}
    lex_words = sum(map(len, all_tags.values()))
    return (lex_words/word_count(text))*100


# calculate the Automated Readability Index (ARI)
def ARI(text):
    words = word_count(text)
    characters = char_count_nospace(text)
    sentences = sentence_count(text)
    return int(4.71*(characters/words) + 0.5*(words/sentences) - 21.43)



