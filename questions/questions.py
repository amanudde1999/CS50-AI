import nltk
import sys
import string
from math import log
import os
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
    corpus = dict()

    for filename in os.listdir(directory):
        pathToFile = os.path.join(directory, filename)
        # Ensuring we only pick files that actually exist with the .txt extension
        if os.path.isfile(pathToFile) and filename.endswith(".txt"):
            with open(pathToFile, "r", encoding= 'utf8') as file:
                # Map filename to the file's contents as a string
                corpus[filename] = file.read()
    return corpus 



def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokenised = nltk.word_tokenize(document.lower())
    tokenisedClean = []
    punctuation = string.punctuation
    stopwords = nltk.corpus.stopwords.words("english")

    for words in tokenised:
        # If there is punctuation
        if words in punctuation:
            # Nothing to do...start at next iteration
            continue
        # If there is a stopword
        elif words in stopwords:
            continue 
        else:
            tokenisedClean.append(words)
    
    return tokenisedClean
    


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    
    # idf = ln(numDocuments/numDocuments word appears in)
    
    numDocuments = len(documents)
    # Dict that will map words to their respective idf values
    idfs = dict()
    documentsWords = []

    for key in documents:
        # Name of document
        document = documents[key]
        for words in document:
            # Creation of keys for idf dictionary
            if words not in documentsWords:
                documentsWords.append(words)
    
    for words in documentsWords:
        wordCount = 0 
        for key in documents:
            document = documents[key]
            if words in document:
                wordCount += 1
                continue
        # Calculate idf for EACH words and add 1 to smooth
        idfs[words] = 1 + log(numDocuments/wordCount)
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = dict()

    for file in files:
        tf_idfs[file] = 0
        # Find number of words
        fileTokens = len(files[file])
        for words in query:
            if words in files[file]:
                Freq = files[file].count(words) + 1
            else:
                # Smoothing for the case that there is no evidence
                Freq = 1
            termFreq = Freq/fileTokens
            # Per specification, only take into account words that appear in the query
            if words in idfs.keys():
                idf = idfs[words]
            else:
                # No evidence case so we dont end up multiplying zero
                idf = 1
            # Find the summation of tf*idf values for ranking 
            tf_idfs[file] += idf * termFreq
    # Ranking according to highest to lowest tf-idf values
    ranking = sorted(tf_idfs, key = tf_idfs.get, reverse = True)
    rankedFiles = ranking[:n]

    return rankedFiles

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentencesRanked = list()
    
    for sentence in sentences:
        sentenceVals = [sentence, 0, 0]

        for word in query:
            if word in sentences[sentence]:
                # Calculating the matching word measure by summing idf values (matching word measure)
                sentenceVals[1] += idfs[word]
                # Calculating the query term density for the word
                sentenceVals[2] += sentences[sentence].count(word) / len(sentences[sentence])

        sentencesRanked.append(sentenceVals)
    # Sort by matching word measure first then query term density
    sentencesRanked = sorted(sentencesRanked, key=lambda i: (i[1],i[2]), reverse = True)[:n]
        
    return [sentence for sentence, MatchingWordMeasure, QuantityTermDensity in sentencesRanked]
    

    

if __name__ == "__main__":
    main()
