#!/usr/bin/env python3

import argparse
import sys
from main import read_grammar

def format_predict_sets(predict_sets, grammar):
    """
    Format PREDICT sets for display, grouped by variable.
    """
    # Group rules by left-hand side variable
    rules_by_var = {}
    for rule in grammar.rules:
        lhs = rule[0]
        if lhs not in rules_by_var:
            rules_by_var[lhs] = []
        rules_by_var[lhs].append(rule)
    
    output_lines = []
    output_lines.append("PREDICT SETS:")
    output_lines.append("=" * 50)
    
    # Process variables in order, starting with start variable
    variables = list(rules_by_var.keys())
    if grammar.start_variable in variables:
        variables.remove(grammar.start_variable)
        variables.insert(0, grammar.start_variable)
    
    for var in variables:
        output_lines.append(f"\nVariable {var}:")
        for rule in sorted(rules_by_var[var], key=lambda r: r[1]):
            lhs, rhs = rule
            predict_set = predict_sets[rule]
            predict_str = '{' + ', '.join(sorted(predict_set)) + '}' if predict_set else '∅'
            output_lines.append(f"  {lhs} → {rhs}  :  {predict_str}")
    
    return '\n'.join(output_lines)

def main():
    parser = argparse.ArgumentParser(description="Compute and display PREDICT sets for a grammar")
    parser.add_argument('grammar_file', help='Path to grammar file')
    args = parser.parse_args()
    
    try:
        grammar = read_grammar(args.grammar_file)
        predict_sets = grammar.compute_predict_sets()
        
        print("GRAMMAR:")
        print("-" * 30)
        print(f"Variables: {sorted(grammar.variables)}")
        print(f"Terminals: {sorted(grammar.terminals)}")
        print(f"Start variable: {grammar.start_variable}")
        print()
        
        print(format_predict_sets(predict_sets, grammar))
        
    except FileNotFoundError:
        print(f"Error: Grammar file '{args.grammar_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
