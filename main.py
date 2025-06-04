import random


def read_grammar(file_path):
    """Read and validate grammar definitions from a text file."""
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

    overlap = set(V) & set(E)
    if overlap:
        raise ValueError(f"Non-terminals and terminals overlap: {overlap}")
    if S not in V:
        raise ValueError(f"Start symbol '{S}' not found in non-terminals V")
    for lhs, alts in R.items():
        if lhs not in V:
            raise ValueError(f"Production rule LHS '{lhs}' not in non-terminals V")
        for alt in alts:
            symbols = [] if alt == 'ε' else list(alt)
            for sym in symbols:
                if sym not in V and sym not in E:
                    raise ValueError(f"Symbol '{sym}' in production '{lhs}->{alt}' not in V or Σ")
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
            symbols = symbols[:i] + replacement + symbols[i + 1:]
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
    cache = {}

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

        key = ''.join(current)
        if key in cache:
            path.pop()
            ops.pop()
            return cache[key]

        result = False
        for i, sym in enumerate(current):
            if sym in R:
                for prod in R[sym]:
                    replacement = [] if prod == 'ε' else list(prod)
                    next_form = current[:i] + replacement + current[i + 1:]
                    if dfs(next_form, depth + 1, f"{sym}->{prod}"):
                        result = True
                        break
                if result:
                    break

        cache[key] = result
        if not result:
            path.pop()
            ops.pop()
        return result

    if dfs([S], 0):
        return list(zip(path, ops)), True
    else:
        return None, False

def recognizer(target, V, E, R, S):
    result, success = derivation(target, V, E, R, S)
    return success


if __name__ == '__main__':
    V, E, R, S = read_grammar('input.txt')
    print_grammar(V, E, R, S)

    generated = stringGenerate(V, E, R, S)

    print('Generated strings:')
    for s in generated:
        print(s if s != '' else 'ε')

    target = input('Enter a target string to derive: ')
    result, success = derivation(target, V, E, R, S)
    if not success:
        print(f'Target "{target}" cannot be derived within depth 15.')
        print(f'The string "{target}" cannot be derived from the grammar.')
    else:
        print(f'The string "{target}" can be derived from the grammar.')
        print('Derivation steps:')
        for form, op in result:
            if op:
                print(f"{form}   ({op})")
            else:
                print(form)

    target = input('Enter a target string to recognize: ')
    if recognizer(target, V, E, R, S):
        print(f'The string "{target}" is recognized by the grammar.')
    else:
        print(f'The string "{target}" is not recognized by the grammar.')