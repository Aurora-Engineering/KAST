from typing import List

from .knowledge.predicate import Predicate
import operator as op

def binary_operators_user_input():
    op_mappings = {'<': op.lt, # Create a mapping of string reps of comparison operators to functions to make these attributes evaluatable
                   '<=': op.le,
                   '==': op.eq,
                   '!=': op.ne,
                   '>': op.gt,
                   '>=': op.lt}
    # toy version of SME defining predicates ahead of time
    # Want SMEs to define predicates in their own terms (since they'll also be defining high level data products)
    new_variable = input("Please enter the name of the variable considered by the predicate: ") # What variable will this predicate operate on?
    if new_variable == "STOP": # Break case
        return None
    binary_operator = input("Please enter one of the follow operators [<,<=,==,!=,>,>=]: ") # What comparison is used for this operation?
    numerical_val = input("Please enter a numerical value: ") # What's the threshold/value this variable will be compared to using the above operator?
    pred_name = input("Please enter a predicate descriptor: ") # What information does this predicate describe? (ex. AtHome, InGripper)

    pred = Predicate(new_variable,op_mappings[binary_operator],numerical_val)
    print(f'Returning: ({pred_name}: {pred})')
    return({pred_name: pred})

def tbinary_operators():
    pass