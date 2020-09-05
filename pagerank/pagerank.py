import os
import random
import re
import sys
from pomegranate import DiscreteDistribution,ConditionalProbabilityTable,MarkovChain



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
    distribution = dict()
    numLinks = len(corpus[page])

    if numLinks != 0:
        # This is the case where the user chooses one out of all the pages in the corpus at random
        for link in corpus:  
            distribution[link] = (1 - damping_factor)/len(corpus)
        for link in corpus[page]:
            distribution[link] += damping_factor/numLinks
    # Otherwise if the page has no outgoing links
    else:
        # We get a distribution where the probability of picking any page is equal to 1/n
        for link in corpus:
            distribution[link] = 1/len(corpus)

    return distribution   

def sample_pagerank(corpus, damping_factor, n):  
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pageRank = dict()
    for page in corpus:
        pageRank[page] = 0
        
    # We choose a page at random
    page = random.choice(list(corpus.keys()))

    # We sample from the first page to the (n-1)th page, since n is at least 1
    for i in range(1, n):
        # Using the current PageRank we obtain a distribuion 
        currentDistribution = transition_model(corpus, page, damping_factor)
        for page in pageRank:
            # We generate the next sample based off of the previous one (i-1)
            pageRank[page] = ((i-1) * pageRank[page] + currentDistribution[page]) / i
        
        page = random.choices(list(pageRank.keys()), list(pageRank.values()), k=1)[0]

    return pageRank

def findLinks(corpus,cPage):

    """
    Returns the the links so we can calculated a page's PageRank
    """

    foundLinks = []
    pages = list(corpus.keys())
    for page in pages:
        if cPage in corpus[page]:
            foundLinks.append(page)

    return foundLinks



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageRank = dict()
    pages = list(corpus.keys())
    flag = 1
    # Assign each page a rank of 1/N
    for page in pages:
        pageRank[page] = 1/len(pages)
    

    while flag == 1:
        probRandom = (1 - damping_factor)/len(pages)
        flag = 0
        for page in pages:
            summation = 0
            links = findLinks(corpus,page)
            for link in links:
                # Keep summing
                summation += pageRank[link]/len(corpus[link])
            # Multiply by the damping factor once since it is outside the summation (const)
            summation *= damping_factor
            difference = abs(pageRank[page] - (probRandom + summation))
            # Keep iterating until no PageRank values change by greater than 0.001
            if difference > 0.001:
                flag = 1
            pageRank[page] = probRandom + summation

    return pageRank


if __name__ == "__main__":
    main()