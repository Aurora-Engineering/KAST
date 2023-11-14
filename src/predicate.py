#!/usr/bin/env python
from abc import ABC, abstractmethod # Should eventually make this an abstract superclass

class Predicate(object):
    def __init__(self, _name, _reference_variable, _operator, _vars):
        self.name = _name
        self.reference_variable = _reference_variable
        self.operator = _operator 
        self.vars = _vars
        
    def __str__(self):
        _vars = ''
        for v in self.vars:                
            _vars = _vars + ' ' + str(v)
        return f'({self.name}: {self.reference_variable} {self.operator.__name__} {self.vars})'
