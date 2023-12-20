from abc import ABC, abstractmethod # Should eventually make this an abstract superclass
import operator as op

OPERATOR_MAPPINGS = {'<': op.lt, # Create a mapping of string reps of comparison operators to functions to make these attributes evaluatable
                    '<=': op.le,
                    '==': op.eq,
                    '!=': op.ne,
                    '>': op.gt,
                    '>=': op.lt}

def get_binary_op_mappings(operator_string: str):
    try:
        op_functional = OPERATOR_MAPPINGS[operator_string]
    except KeyError as e:
        raise KeyError(f'Given operator {operator_string} is not contained in the binary operator mappings list. Check syntax.')
    else:
        return(op_functional)

class Predicate(object):
    def __init__(self, _name, _reference_variable, _operator, _vars):
        self.name = _name
        self.reference_variable = _reference_variable
        self.operator = get_binary_op_mappings(_operator)
        self.vars = _vars
        
    def __str__(self):
        _vars = ''
        for v in self.vars:                
            _vars = _vars + ' ' + str(v)
        return f'({self.name}: {self.reference_variable} {self.operator.__name__} {self.vars})'
