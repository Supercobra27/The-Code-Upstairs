from collections import defaultdict

def compute_first_sets(grammar):
    first = defaultdict(set)
    
    def first_of(symbol):
        if symbol in first:
            return first[symbol]
        if symbol.islower():  # Assuming lowercase are terminals
            first[symbol].add(symbol)
            return first[symbol]
        
        for production in grammar[symbol]:
            for sym in production:
                sym_first = first_of(sym)
                first[symbol].update(sym_first - {'ε'})
                if 'ε' not in sym_first:
                    break
            else:
                first[symbol].add('ε')
        return first[symbol]
    
    for non_terminal in grammar:
        first_of(non_terminal)
    return first

def compute_follow_sets(grammar, first):
    follow = defaultdict(set)
    start_symbol = next(iter(grammar))
    follow[start_symbol].add('$')  # Assume $ is the end of input marker

    def follow_of(symbol):
        for head, productions in grammar.items():
            for production in productions:
                if symbol in production:
                    for i, sym in enumerate(production):
                        if sym == symbol:
                            next_symbols = production[i+1:]
                            if next_symbols:
                                first_next = set()
                                for next_symbol in next_symbols:
                                    first_next.update(first[next_symbol] - {'ε'})
                                    if 'ε' not in first[next_symbol]:
                                        break
                                else:
                                    first_next.add('ε')
                                follow[symbol].update(first_next - {'ε'})
                                if 'ε' in first_next:
                                    follow[symbol].update(follow[head])
                            else:
                                follow[symbol].update(follow[head])
    
    for _ in grammar:
        for non_terminal in grammar:
            follow_of(non_terminal)
    return follow

# Example Grammar
grammar = {
    'S': [['A', 'B'], ['C']],
    'A': [['a'], ['ε']],
    'B': [['b']],
    'C': [['c'], ['A']]
}

first_sets = compute_first_sets(grammar)
follow_sets = compute_follow_sets(grammar, first_sets)

print("First Sets:", dict(first_sets))
print("Follow Sets:", dict(follow_sets))
