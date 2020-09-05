import nltk
import sys


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S P S | VP NP | S P NP | S NP 
AP -> Adj | Adj AP
NP -> N | Det N | Det AdjAdv N | P NP | Det N AdjAdv | AdjAdv N | NP Adv V
AdjAdv -> Adj | Adj AdjAdv | Adv
VP -> V | V P NP | Adv V | V AdjAdv | V P
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # I would have importted string and used list(string.ascii_lowercase) but im not sure if string lib is allowed 
    allowed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    # Change to lowercase and tokenise
    tokenised = nltk.word_tokenize(sentence.lower())
    tokenisedClean = []

    # We begin the filtering process here
    for words in tokenised:
        for letters in words:
            if letters in allowed:
                tokenisedClean.append(words)
                # Use break here to get out of the inner for loop and check the next word
                break
            else:
                # Otherwise it does not contain AT LEAST one alphabetic letter and we leave it
                continue

    return tokenisedClean


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    NPChunks = []
    # Iterate over all subtrees and if any are NP we add them to our NPChunks list
    for subtrees in tree.subtrees():
        if (subtrees.label() =='NP'):
            NPChunks.append(subtrees)
    
    return NPChunks


if __name__ == "__main__":
    main()
