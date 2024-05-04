# TP Implementation of the Earley algorithm (with pred function)
from EarlyParser.CFGParsingClasses import Symbol, Rule, Grammar
from EarlyParser.earlyParser import parse_earley

# This is the main script to test the Earley Parser we define toy grammars including a CFG for natural language
# The grammars which were part of the original document uploaded to moodle are put in multiline quotes
# which accepts the "book that flight" example

if __name__ == "__main__":

    # A NL grammar for 'book that flight example'
    # initialize symbols
    symS = Symbol("S")
    symAux = Symbol("Aux")
    symNP = Symbol("NP")
    symVP = Symbol("VP")
    symDet = Symbol("Det")
    symV = Symbol("V")
    symNoun = Symbol("Noun")

    # terminals...
    symTerminalBook = Symbol("book")
    symTerminalThat = Symbol("that")
    symTerminalFlight = Symbol("flight")
    symTerminalDoes = Symbol("does")

    # definition of a very short NL grammar
    nl_grammar = Grammar(
        # sigma and N
        symbols=[symS,
                 symAux,
                 symNP,
                 symVP,
                 symDet,
                 symNoun,
                 symV,
                 symTerminalBook,
                 symTerminalThat,
                 symTerminalFlight,
                 symTerminalDoes],
        # S
        axiom=symS,

        # P
        rules=[
            Rule(lhs=symS, rhs=[symNP, symVP]),
            Rule(lhs=symS, rhs=[symAux, symNP, symVP]),
            Rule(lhs=symS, rhs=[symVP]),
            Rule(lhs=symNP, rhs=[symDet, symNoun]),
            Rule(lhs=symVP, rhs=[symV]),
            Rule(lhs=symVP, rhs=[symV, symNP]),
            Rule(lhs=symV, rhs=[symTerminalBook]),
            Rule(lhs=symDet, rhs=[symTerminalThat]),
            Rule(lhs=symAux, rhs=[symTerminalDoes]),
            Rule(lhs=symNoun, rhs=[symTerminalFlight]),
        ],
        name="NL grammar"
    )

    # we need some iterative to iterate over words in a natural language sentence the same way we would iterate over the tokens of a word in a formal language
    word = "book that flight".split()

    print("-------------------natural language grammar-------------------")
    print(nl_grammar)
    parse_earley(nl_grammar, word)