import argparse
from cfg import CFG
from main import read_grammar

def pretty_lower_left(V):
    """
    Print the CYK table so that:
      • V[0][-1] (the ‘answer’ cell) is at the top-left;
      • Only the lower-left triangular part is displayed.
    """
    n = len(V)
    for span in range(n-1, -1, -1):          # top row has longest span
        row_cells = []
        for i in range(n - span):             # i = left index of the span
            j = i + span                      # right index
            cell = V[i][j]
            txt = '{' + ','.join(sorted(cell)) + '}' if cell else '∅'
            row_cells.append(f'{txt:8}')
        print(' '.join(row_cells))

def main():
    parser = argparse.ArgumentParser(description="Single CYK check with optional matrix display")
    parser.add_argument('grammar')
    parser.add_argument('word')
    parser.add_argument('-m', '--matrix', action='store_true', help='print CYK matrix')
    args = parser.parse_args()

    g = read_grammar(args.grammar)
    ok, V = g.cyk_matrix(args.word, return_table=True)
    print(f"String '{args.word}'  ->  {'ACCEPTED' if ok else 'REJECTED'}")
    if args.matrix:
        print("CYK table (lower-left triangle, V[0][-1] in top-left):")
        pretty_lower_left(V)

if __name__ == '__main__':
    main()
