import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.
    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probability = float(1)

    for person in people:
        # Assign values depending on how many of the gene the person has
        genes = (
            2 if person in two_genes 
            else 1 if person in one_gene 
            else 0
        )

        trait = person in have_trait
        mother = people[person]["mother"]
        father = people[person]["father"]

        # Find the unconditional probability if no parents are registered
        if father is None and mother is None:
            # We use the values defined in PROBS
            probability *= PROBS["gene"][genes]

        # If there are registered parents, we use their values and there is a mutation chance
        else:
            passing = {mother: 0, father: 0}

            for parent in passing:
                passing[parent] = (
                    # If the parents has two genes then it will definitely mutate 
                    1 - PROBS["mutation"] if parent in two_genes 

                    # If only one gene then there is a 50% chance of mutation
                    else 0.5 if parent in one_gene 

                    # If
                    else PROBS["mutation"]
                )

            probability *= (
                # Both parents passing the gene
                passing[mother] * passing[father] if genes == 2 

                # Either the father or the mother give the gene (not both simultaneously condition)
                else passing[mother] * (1 - passing[father]) + (1 - passing[mother]) * passing[father] if genes == 1 

                # Not getting the gene from the pather or mother
                else (1 - passing[mother]) * (1 - passing[father])
            )

        probability *= PROBS["trait"][genes][trait]

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # Make a list of all the individuals so we can go through all of them and update the probabilities
    persons = list(probabilities.keys())
    # Adding p to the appropriate value in each distribution 
    for person in persons:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # Make a list of all the individuals so we can go through all of them and normalise
    people = list(probabilities.keys())

    for person in people:
        probSum = 0
        # Go through all 3 numbers of genes (0,1,2)
        for i in range(3):
            # Find the sum of all the probabilities of all the different number of genes for that person
            probSum += probabilities[person]["gene"][i]

        for i in range(3):
            # Divide by the sum to normalise 
            probabilities[person]["gene"][i] /= probSum

        # We do the same as above for the trait variable
        probSum = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        # Divide by the sum to normalise
        probabilities[person]["trait"][True] /= probSum
        probabilities[person]["trait"][False] /= probSum

if __name__ == "__main__":
    main()