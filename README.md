# Grammar Parser and Recognizer

This program allows you to work with context-free grammars. It can:
- Parse grammar definitions from a file
- Generate random strings from the grammar
- Check if a string can be derived from the grammar
- Show the derivation steps for a given string

## How to Run

1. Make sure you have Python 3 installed
2. Clone the repository:
   ```
   git clone https://github.com/MihaiPMC/ContextFreeGrammar
   ```
3. Navigate to the project directory:
   ```
   cd ContextFreeGrammar
   ```
4. Create an input file (default: `input.txt`) with your grammar definition or use the provided example
5. Run the program:
   ```
   python main.py
   ```
6. Follow the prompts to interact with the program

## Input File Format

The input file should follow this format:
```text
<n>                   # number of non-terminals
<NT₁>
...
<NTₙ>
<m>                   # number of terminals
<T₁>
...
<Tₘ>
<p>                   # number of production rules
<LHS₁> -> <alt₁₁> | <alt₁₂> | ...
...
<LHSₚ> -> <altₚ₁> | <altₚ₂> | ...
<k>                   # length limit or unused in this context
<S>                   # start symbol
```

For example:
```text
1
S
2
a
b
1
S -> aS | Sb | aSb | ε
1
S
```

## Example Output

```text
V = ['S']
E = ['a', 'b']
R =
S -> aS | Sb | aSb | ε
S = S

Generated strings:
aaabbbbb
aa
b
ε
aaaabbbbb
ε
ab
ε
ab
aabb

Enter a target string to derive: aab
The string "aab" can be derived from the grammar.
Derivation steps:
S
aS   (S->aS)
aaS   (S->aS)
aaSb   (S->Sb)
aab   (S->ε)

Enter a target string to recognize: aba
The string "aba" is not recognized by the grammar.
```

## Code Overview

- **read_grammar(file_path)**  
  Reads counts and symbols from the input file, builds and validates `V`, `E`, `R`, and start symbol `S`.
- **print_grammar(V, E, R, S)**  
  Nicely prints the sets of non-terminals, terminals, production rules, and start symbol.
- **stringGenerate(V, E, R, S)**  
  Randomly expands non-terminals up to `MAX_GENERATED` strings, avoiding too-long outputs.
- **derivation(target, V, E, R, S)**  
  Uses DFS with depth limit `MAX_DEPTH` and memoization to find a derivation path or fail.
- **recognizer(target, V, E, R, S)**  
  Wraps `derivation` to return a simple boolean recognition result.
