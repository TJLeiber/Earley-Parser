# module containing auxiliary functions to Earley parsing algorithm and algorithm itself

from EarlyParser.CFGParsingClasses import Item, TableCell

def advance_dot(it):
    '''takes an object of class item as input and returns a new object instance where the dot in the rule has been advanced by one'''
    # it: Item

    # returns new item which has rule with the dot advanced by one position

    # to advance the dot we create a list 'bd' containing everything before the dot in 'it' (Item) plus the first thing after the dot
    new_bd = [symb for symb in it.bd]

    # move first token which appears after the dot in front of the dot
    new_bd.append(it.ad[0])

    # get a list of everything which remains, i.e. everything after the dot except for the first token which has been moved in front of the dot
    new_ad = [symb for symb in it.ad[1:]]

    # create the new item where the dot is advanced
    new_item = Item(i=it.i, lhs=it.lhs, bd=new_bd, ad=new_ad)

    return new_item

# Creation and initialisation of the table T for the word w and the grammar gr
def init(g, w):
    '''initializes the chart for early parsing with all initial 'axiom'-states in the first cell'''
    # g: Grammar
    # w: word

    # initialize the chart as a dictionary with tokens of word as keys and TableCell objects as respective values
    # TableCell objects have a list, i.e. an ordered multiset as an attribute, and a cAppend method to append.
    T = {i: TableCell() for i in range(len(w) + 1)}

    # now we add all
    for rule in g.rules:
        # for each rule compare its string representation with the string representation of the grammars axiom
        if rule.lhs.name == g.axiom.name:

            # a state corresponding to a rule which starts at the axiom
            axiom_state = Item(i=0, lhs=g.axiom, bd=[], ad=rule.rhs)

            # add the item corresponding to all dot initial rules which rewrite the axiom
            T[0].cAppend(axiom_state, reason="init")

    return T

# Insert in the table any new items resulting from the pred operation for the iterm it
def pred(g, it, T,j):
    '''generates a new state representing a top-down expectation;
    i.e. creates a new item if symbol following dot is a non-terminal;
    the new item represents a constituent at with the same span, but the non-terminal on the lhs and its children
     in the respective rule of the grammar as its children'''
    # g: Grammar
    # it: Item
    # T: table
    # j : index

    # look at the token which appears after the dot in the early item
    first_after_dot = it.ad[0] # won't cause index error because comp is checked previously (?)

    # check if the token is a non-terminal
    if g.isNonTerminal(first_after_dot):
        # loop over all rules in the given grammar
        for rule in g.rules:
            # if the str repr. of the lhs of a rule is equal to the str repr. the non-terminal before dot in item
            if rule.lhs.name == first_after_dot.name:
                # create item which is the 'expansion' item of an item to which pred applies
                scan_item = Item(i=j, lhs=first_after_dot, bd=[], ad=rule.rhs)
                # append the expansion state in the same cell
                T[j].cAppend(scan_item, reason="pred")

# Insert in the table any new items resulting from the scan operation for the iterm it
def scan(it,T,j):
    '''operation in early parsing algorithm, which is applied if an item is scannable;
     creates a new rule with the dot advanced and pushes it on next cell'''
    # it: Item
    # T: table
    # j: index

    # advance the dot
    new_item = advance_dot(it)

    # append the new item to the cell at the next index
    T[j + 1].cAppend(new_item, reason="scan")

# Insert in the table any possible new items resulting from the comp operation for the iterm it
def comp(it,T,j):
    # it: Item
    # T: table
    # j: index

    # go through all the items at the cell where the span of the item which triggered comp starts
    k = 0 # variable to loop over items at the origin index of the item which triggered comp
    origin_idx = it.i # origin idx of the item which triggered comp (will be the key in the table to look at)

    while k < len(T[origin_idx]): # actual loop condition

        # take an item at the origin cell
        sample_item = T[it.i][k]

        # look at its char appearing after the dot
        # error handling to prevent index errors (when the sampled rule is a dot-last rule)
        try:
            first_after_dot = sample_item.ad[0].name # string repr. of a symbol object

        # if the sampled rule is a dot-last rule then a forteriori it is not a rule s.t. it is waiting for the lhs of it (triggering Item)
        except IndexError:
            # hence we disregard the item by incrementing k and continuing
            k += 1
            continue

        # get the triggering items left hand side
        left_hand_side = it.lhs.name

        # check if the sampled rule is 'waiting' for the triggering rule's lhs
        if first_after_dot == left_hand_side:

            # advance the dot on the rule which can be completed with the already accepted item (the one which triggered comp)
            new_item = advance_dot(sample_item)

            # append the rule to the current cell
            T[j].cAppend(new_item, reason="comp")

        k +=1 # increment the counter to look at the next item in the cell



# Return True if the analysis is successful, otherwise False
def table_complete(g, w, T):
    '''given a table a word and a grammar this function returns True if the following condition holds:
    ∃α, (S → α •, 0) ∈ T[len(w)] i.e. there is a rule starting from the axiom, spanning the entire word which is recognized as a constituent'''

    # g: Grammar
    # w: word
    # T: table

    # string repr. of the axiom
    axiom = g.axiom.name

    # key of the last cell
    last_cell = len(w)

    for item in T[last_cell]:
        if (item.i == 0) and (not item.ad) and (item.lhs.name == axiom):
            return True

    return False

# Parse the word w for the grammar g return the parsing table at the end of the algorithm
def parse_earley(g, w):
    # g: Grammar
    # w: word


    # Initialisation
    T = init(g,w)

    # Top-down analysis

    # loop over keys in the table, i.e. 0 to |w|
    for j in range(len(w) + 1):
        k = 0 # reset k to loop over the cell at the current index j
        while k < len(T[j]): # length of the list attribute of the TableCell object
            probed_item = T[j][k] # we take the item corresponding to the current indices and check whether some operation should apply or not

            # check if comp may be performed, i.e. if the current item is an accepted (dot last one)
            if not probed_item.ad: # True if ad is an empty list, i.e. nothing after the dot
                comp(probed_item, T, j) # implements the loop over the relevant items at the origin idx of probed_item

            # check if pred may be performed, i.e. if the token after the dot is a non-terminal
            elif g.isNonTerminal(probed_item.ad[0]): # true if first token after the dot is a non-term in the given grammar
                pred(g, probed_item, T, j)

            # check if scan may be performed, i.e. when we are not at the last cell (still parsing constituents of w)
            elif j < len(w):
                # check if the first token after the dot is the same as the token in the word at the current index
                if probed_item.ad[0].name == w[j]:
                    scan(probed_item, T, j)

            k += 1 # increment k by one to probe the next item at in the current cell

    if table_complete(g, w, T):
        print("Success")
    else:
        print("Failed parsing")

    return T

# --------------