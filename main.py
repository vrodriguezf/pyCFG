import sys
import re
from tabulate import tabulate
import pandas as pd

# Assuming pyCFG is saved in a file named pyCFG.py in the same directory
from cfg import *

def read_grammar(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # BOTCH: This is a hack to make 0's and 1's as a's or b's, a bug in cfg
        lines = [re.sub(r'0', 'a', re.sub(r'1', 'b', re.sub(r'2', 'c', line))) for line in lines]
    
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


def main(grammar_file, positive_strings_file=None, negative_strings_file=None):
    g = read_grammar(grammar_file)
    print("---- GRAMMAR ----")
    print(g)

    # Indicate if the grammar is in Chomsky Normal Form
    print(f"Chomsky Normal Form: {'Yes' if g.is_chamsky() else 'No'}")
    
    # Indicate if the grammar is regular
    print(f"Regular Grammar: {'Yes' if g.is_regular() else 'No'}")

    # Indicate if the grammar is LL(1)
    print(f"LL(1) Grammar: {'Yes' if g.is_ll1() else 'No'}")
    
    if positive_strings_file:
        with open(positive_strings_file, 'r') as file:
            p_strings = [line.strip() for line in file if line.strip()]
            p_strings_for_show = {"String": [], "Is Accepted": []}
        for p_string in p_strings:
            p_strings_for_show["String"].append(p_string)
            if p_string == 'ε':
                p_strings_for_show["Is Accepted"].append(g.accepts_null)
            else:
                # BOTCH: This is a hack to make 0's and 1's as a's or b's, a bug in cfg
                p_strings_for_show["Is Accepted"].append(
                    g.cyk(re.sub(r'0', 'a', re.sub(r'1', 'b', re.sub(r'2', 'c', p_string))))
                )
            #p_strings_for_show["Is Accepted"].append(g.cyk(p_string))
        p_strings_df = pd.DataFrame(p_strings_for_show)
        print(f"\nPositive Tests:\n{tabulate(p_strings_df, headers='keys', tablefmt='fancy_grid')}")

    if negative_strings_file:
        with open(negative_strings_file, 'r') as file:
            n_strings = [line.strip() for line in file if line.strip()]
            n_strings_for_show = {"String": [], "Is Rejected": []}
        for n_string in n_strings:
            n_strings_for_show["String"].append(n_string)
            if n_string == 'ε':
                n_strings_for_show["Is Rejected"].append(not g.accepts_null)
            else:
                # BOTCH: This is a hack to make 0's and 1's as a's or b's, a bug in cfg
                n_strings_for_show["Is Rejected"].append(
                    not g.cyk(re.sub(r'0', 'a', re.sub(r'1', 'b', re.sub(r'2', 'c', n_string))))
                )
            # n_strings_for_show["Is Rejected"].append(not g.cyk(n_string))
        n_strings_df = pd.DataFrame(n_strings_for_show)
        print(f"Negative Tests:\n{tabulate(n_strings_df, headers='keys', tablefmt='fancy_grid')}\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <grammar_file> <positive_strings> <negative_strings>")
        sys.exit(1)
    
    grammar_file = sys.argv[1]
    positive_strings_file = sys.argv[2]
    negative_strings_file =sys.argv[3]
    
    main(grammar_file, positive_strings_file, negative_strings_file)
