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
S -> DN VP
DN -> NA | Det NA | Det NA Adv
NC -> DN | DN Conj SA
AA -> Adj | Adj Adj | Adj Adj Adj
AN -> AA NC | NC | AA V | AA V P DN
PD -> P Det | Det
VA -> V | Adv V | V Adv
NA -> N | AA N | AA N PD NC
SA -> S | VA Det N | VA DN PD NA
VP -> VA | VA Conj SA | NP | VA PD AN
DV -> V Det DN | V Det AA V | VA
NP -> DV | DV P DN | DV P DN Conj SA
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
    print ("np chunk. tree: ", tree)
    raise NotImplementedError


if __name__ == "__main__":
    main()
