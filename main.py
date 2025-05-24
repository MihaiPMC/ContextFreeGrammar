import random

def read_grammar(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        n = int(f.readline())
        V = [f.readline().strip() for _ in range(n)]
        m = int(f.readline())
        E = [f.readline().strip() for _ in range(m)]
        p = int(f.readline())
        R = {}
        for _ in range(p):
            line = f.readline().strip()
            lhs, rhs = line.split('->', 1)
            lhs = lhs.strip()
            alts = [alt.strip() for alt in rhs.strip().split('|')]
            R[lhs] = alts
        k = int(f.readline())
        S = f.readline().strip()
    return V, E, R, S

def print_grammar(V, E, R, S):
    print('V =', V)
    print('E =', E)
    print('R =')
    for lhs, alts in R.items():
        print(f'{lhs} -> {" | ".join(alts)}')
    print('S =', S)

def stringGenerate(V, E, R, S):
    def generate_one():
        symbols = [S]
        while any(sym in V for sym in symbols):
            terminals = [sym for sym in symbols if sym in E]
            if len(terminals) > 10:
                return None
            idxs = [i for i, sym in enumerate(symbols) if sym in V]
            i = random.choice(idxs)
            sym = symbols[i]
            alt = random.choice(R[sym])
            if alt == 'ε':
                replacement = []
            else:
                replacement = list(alt)
            symbols = symbols[:i] + replacement + symbols[i+1:]
        result = ''.join(symbols)
        return result if len(result) <= 10 else None

    results, attempts = [], 0
    while len(results) < 10 and attempts < 1000:
        attempts += 1
        s = generate_one()
        if s is not None:
            results.append(s)
    return results

def derivation(target, V, E, R, S):
    path = []
    ops = []

    def dfs(current, depth, op=None):
        sent = ''.join(current) or 'ε'
        path.append(sent)
        ops.append(op)

        if sent == target:
            return True

        if depth >= 15:
            path.pop()
            ops.pop()
            return False

        term_count = sum(1 for sym in current if sym in E)
        if term_count > len(target):
            path.pop()
            ops.pop()
            return False

        for i, sym in enumerate(current):
            if sym in R:
                for prod in R[sym]:
                    replacement = [] if prod == 'ε' else list(prod)
                    next_form = current[:i] + replacement + current[i+1:]
                    if dfs(next_form, depth + 1, f"{sym}->{prod}"):
                        return True

        path.pop()
        ops.pop()
        return False

    if dfs([S], 0):
        print('Derivation path:')
        for form, op in zip(path, ops):
            if op:
                print(f"{form}   ({op})")
            else:
                print(form)
        return True
    else:
        print(f'Target "{target}" cannot be derived within depth 15.')
        return False


if __name__ == '__main__':
    V, E, R, S = read_grammar('input.txt')
    print_grammar(V, E, R, S)

    generated = stringGenerate(V, E, R, S)

    print('Generated strings:')
    for s in generated:
        print(s if s != '' else 'ε')

    target = input('Enter a target string to derive: ')
    derivation(target, V, E, R, S)
