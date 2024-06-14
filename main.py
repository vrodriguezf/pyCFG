import sys
import re

# Assuming pyCFG is saved in a file named pyCFG.py in the same directory
from cfg import *

def read_grammar(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    variables = set()
    terminals = set()
    rules = set()
    start_variable = None
    null_character = None
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        if line.startswith("Variables:"):
            variables = set(line.split(":")[1].strip().split(","))
        elif line.startswith("Terminals:"):
            terminals = set(line.split(":")[1].strip().split(","))
        elif line.startswith("Start:"):
            start_variable = line.split(":")[1].strip()
        elif line.startswith("Null:"):
            null_character = line.split(":")[1].strip()
        else:
            match = re.match(r'(\w+)\s*->\s*(.+)', line)
            if match:
                var, rule = match.groups()
                for subrule in rule.split("|"):
                    rules.add((var.strip(), subrule.strip()))
    
    return CFG(variables, terminals, rules, start_variable, null_character)

def check_strings_with_cyk(grammar, strings):
    results = {}
    for string in strings:
        results[string] = grammar.cyk(string)
    return results

def main(grammar_file, strings_file):
    grammar = read_grammar(grammar_file)
    
    with open(strings_file, 'r') as file:
        strings = [line.strip() for line in file if line.strip()]
    
    results = check_strings_with_cyk(grammar, strings)
    
    for string, result in results.items():
        print(f"'{string}' is in the language: {result}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <grammar_file> <strings_file>")
        sys.exit(1)
    
    grammar_file = sys.argv[1]
    strings_file = sys.argv[2]
    
    main(grammar_file, strings_file)
