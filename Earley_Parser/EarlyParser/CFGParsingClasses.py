# This is the module containing class definitions to construct a CFG plus the Earley specific classes Item and TableCell

class Symbol:
    # field name: String
    # (no methods)

    def __init__(self, name):
        # name: String

        self.name = name

    def __str__(self):
        return self.name


class Rule:
    # field lhs: Symbol
    # field rhs: list of Symbol
    # (no methods)

    def __init__(self, lhs, rhs):
        # lhs: Symbol
        # rhs: list of Symbol

        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str(self.lhs) + " --> [" + ",".join([str(s) for s in self.rhs]) + "]"


class Grammar:
    # field symbols: list of Symbol
    # field axiom: Symbol
    # field rules: list of Rule
    # field nonTerminals: set of Symbol
    # field name: String
    # method createNewSymbol: String -> Symbol
    # method isNonTerminal: Symbol -> Boolean

    def __init__(self, symbols, axiom, rules, name):
        # symbols: list of Symbol
        # axiom: Symbol
        # rules: list of Rule
        # name: String

        self.symbols = symbols
        self.axiom = axiom
        self.rules = rules
        self.name = name

        self.nonTerminals = set()
        for rule in rules:
            self.nonTerminals.add(rule.lhs)

    # Returns a new symbol (with a new name build from the argument)
    def createNewSymbol(self, symbolName):
        # symbolName: String

        name = symbolName

        ok = False
        while (ok == False):
            ok = True
            for s in self.symbols:
                if s.name == name:
                    ok = False
                    continue

            if ok == False:
                name = name + "'"

        return Symbol(name)

    def isNonTerminal(self, symbol):
        # symbol: Symbol

        return symbol in self.nonTerminals

    def __str__(self):
        return "{" + \
               "symbols = [" + ",".join([str(s) for s in self.symbols]) + "] " + \
               "axiom = " + str(self.axiom) + " " + \
               "rules = [" + ", ".join(str(r) for r in self.rules) + "]" + \
               "}"


class Item:
    # field lhs: Symbol
    # field bd: list of Symbol
    # field ad: list of Symbol
    # field i: Integer

    def __init__(self, i,lhs, bd, ad):  # [i,lhs --> bd•ad]
        self.lhs = lhs
        self.bd = bd
        self.ad = ad
        self.i = i

    def __str__(self):
        return "[%d,%s --> %s • %s]" % \
               (self.i, str(self.lhs), ",".join([str(s) for s in self.bd]), ",".join([str(s) for s in self.ad]))

    def __eq__(self, other):
        return self.i == other.i and \
               self.lhs == other.lhs and self.bd == other.bd and self.ad == other.ad

class TableCell:
    # field c: list of Item
    # method cAppend: add Item to table cell


    c = []

    def __init__(self):
        self.c = []

    # I added this function so that the code would be more readable in the main implementation (let's us write len(T[j]) instead of len(T[j].c)
    def __len__(self):
        return len(self.c)

    # I also introduced this for readability purposes, (let's us write T[j][k] instead of T[j].c[k])
    def __getitem__(self, index):
        return self.c[index]


    # Adds an item at the end of the t (+ prints some log), argument reason indicates the name of operations:"init","pred","scan","comp"
    def cAppend(self, item, reason=None):
        if reason != None:
            reasonStr =  reason + ": "
        else:
            reasonStr = ""

        if item not in self.c:
            self.c.append(item)
            print(reasonStr+ str(item) )


# ------------------------
