import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            with open(f) as doc:
                text = doc.read()
            files[filename] = text
    return (files)


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # using the nltk library to split the sentence into a list
    # of individiual words and makes sure everything is lowercase
    words = []
    for t in nltk.tokenize.sent_tokenize(document):
        t = t.lower()
        words += nltk.tokenize.word_tokenize(t)
    # loop through stopwords defined in nltk.corpus.stopwords and
    # loop through string.punctuation to remove any elements in words
    # list that has that value
    for elem in nltk.corpus.stopwords.words("english"):
        words = [x for x in words if x != elem]
    for elem in string.punctuation:
        words = [x for x in words if x != elem]
    return (words)


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    result = {}
    total = len(documents)
    for file in documents:
        for elem in documents[file]:
            if elem not in result:
                # calculate idf
                count = 0
                for f in documents:
                    if elem in documents[f]:
                        count += 1
                idf = math.log((total / count))
                result[elem] = idf
    return (result)


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # initiate function
    ranked = {}
    for file in files:
        ranked[file] = 0
    # loop over words in query to see which ones occures in which files
    for word in query:
        if word in idfs:
            # first calculate words occurence in individual file
            for file in files:
                total = len(files[file])
                count = 0
                for elem in files[file]:
                    if elem == word:
                        count += 1
                tf = count / total
                # add tf-idf value to files total value
                ranked[file] += (tf * idfs[word])
    # sort files into a ranked list depending on value of n
    ranked_list = []
    i = 0
    while i < n:
        top_value = -1
        for elem in ranked:
            if (ranked[elem] > top_value or top_value == -1) and elem not in ranked_list:
                top_file = elem
                top_value = ranked[elem]
        ranked_list.append(top_file)
        i += 1
    return (ranked_list)


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # initialize ranked list of the sentences
    ranked = {}
    for elem in sentences:
        ranked[elem] = 0
    # loop through each word in the query and if they occur in idfs
    # we will see which sentences contains the word and we will add
    # the idf value to that sentences total count
    for word in query:
        if word in idfs:
            for elem in sentences:
                if word in sentences[elem]:
                    ranked[elem] += idfs[word]
    # select the sentences with the highest ranked count
    ranked_list = []
    i = 0
    while i < n:
        top_value = -1
        for elem in ranked:
            if (ranked[elem] >= top_value or top_value == -1) and elem not in ranked_list:
                top_file = elem
                top_value = ranked[elem]
        ranked_list.append(top_file)
        i += 1
    return (ranked_list)


if __name__ == "__main__":
    main()
