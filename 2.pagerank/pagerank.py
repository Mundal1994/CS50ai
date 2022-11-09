import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    result = {}
    N = len(corpus[page])
    if not N:
        for elem in corpus:
            result[elem] = 1 / len(corpus)
    else:
        for elem in corpus:
            result[elem] = (1 - damping_factor) / len(corpus)
        for elem in corpus[page]:
            result[elem] += damping_factor / N
    return result

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    results = {}
    page = random.choice(list(corpus.keys()))
    for i in corpus:
        results[i] = 0
    for i in range(0, n):
        temp = transition_model(corpus, page, damping_factor)
        for site in results:
            results[site] = (i * results[site] + temp[site]) / (i + 1)
        page = random.choices(list(results.keys()), list(results.values()), k=1)[0]
    return results

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    results = {}
    N = len(corpus)
    for i in corpus:
        results[i] = 1 / N
    i = 0
    while i < N:
        i = 0
        for elem in corpus:
            nbr = (1 - damping_factor) / N
            total = 0
            for site in corpus:
                if elem in corpus[site]:
                    total += results[site] / len(corpus[site])
            total *= damping_factor
            nbr += total
            if abs(results[elem] - nbr) <= 0.0001:
                i += 1
            results[elem] = nbr
    return results

if __name__ == "__main__":
    main()
