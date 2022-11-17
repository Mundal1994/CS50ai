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
S -> NP | NP VP | VP | S Conj S | S P S
AA -> Adj | Adj Adj | Adj Adj Adj
NP -> N | AA N | Adv NP | N Adv | Det N | Det NP | P NP
VP -> V NP | V | Adv VP | V Adv
"""
# First attempt
# works but sometimes tree looked a bit wierd and had issues with np_chunk
# so had to try and make a simpler version
#S -> NP VP
#NP -> NA | Det NA | Det NA Adv
#NC -> NP | NP Conj SA
#AA -> Adj | Adj Adj | Adj Adj Adj
#AN -> AA NC | NC | AA V | AA V P NP
#PD -> P Det | Det
#VA -> V | Adv V | V Adv
#NA -> N | AA N | AA N P NC
#SA -> S | VA Det N | VA NP PD NA
#VP -> VA | VA Conj SA | NV | VA P AN | VA AN
#DV -> V Det NP | V Det AA V | VA
#NV -> DV | DV P NP | DV P NP Conj SA

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
    # using the nltk library to split the sentence into a list
    # of individiual words and makes sure everything is lowercase
    for t in nltk.tokenize.sent_tokenize(sentence):
        t = t.lower()
        words = nltk.tokenize.word_tokenize(t)
    # loop through each word to check if they contain alphabetic value
    # if it doesn't it will be removed
    for elem in words:
        alpha = False
        for char in elem:
            if char.isalpha():
                alpha = True
        if not alpha:
            words.remove(elem)
    return (words)

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    for subtree in tree:
        for children in subtree.subtrees(filter=lambda t: t.label()=='NP' and len(t) >= 1):
            for elem in chunks:
                if children in elem:
                    chunks.pop()
            chunks.append(children)
    return (chunks)

if __name__ == "__main__":
    main()
