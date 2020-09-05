from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Structure of the problem

    # A is either a knight or a knave
    Or(AKnight,AKnave),
    # But if A is a knight then it is NOT a knave and vice-versa
    Implication(AKnave, Not(AKnight)),
    Implication(AKnight, Not(AKnave)),

    # From the given statement
    Biconditional(AKnight, And(AKnave,AKnight))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Same logic as Puzzle 0 for both A and B
    Or(AKnight,AKnave),
    Implication(AKnight,Not(AKnave)),
    Or(BKnight,BKnave),
    Implication(BKnight, Not(BKnave)),
    # From the given statements
    # If A is telling the truth i.e. it is a knight then...
    # A is a knave and B is a knave
    Biconditional(AKnight, And(AKnave,BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Same structure as Puzzle 1
    Or(AKnight, AKnave),
    Implication(AKnight, Not(AKnave)),
    Or(BKnight,BKnave),
    Implication(BKnight, Not(BKnave)),

    # Contradictary statements in the given info so
    # using A AND B's statements
    And(
        # B's statement
        Biconditional(BKnight,Or(
                                    And(AKnight,Not(BKnight)),
                                    And(Not(AKnight),BKnight)
                                )
        ),
        # A's statement
        Biconditional(AKnight, Or(
                                    And(AKnight,BKnight),
                                    And(Not(AKnight),Not(BKnight))
                                ) 
        )
    )
)
# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    Or(AKnight,AKnave),
    Implication(AKnight,Not(AKnave)),

    Or(BKnight,BKnave),
    Implication(BKnight,Not(BKnave)),

    Or(CKnight,CKnave),
    Implication(CKnight,Not(CKnave)),
    
    # A's statement
    Or(Biconditional(AKnight,AKnight), Biconditional(AKnight,AKnave)),

    # C's statement
    Biconditional(CKnight, AKnight),
        
    # B's statement 
    Biconditional(BKnight,Not(CKnight)),
    Biconditional(BKnight, Biconditional(AKnight,AKnave))

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
