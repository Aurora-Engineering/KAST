#!/usr/bin/env python

class Predicate(object):
    def __init__(self, _operator, _vars):
        self.operator = _operator
        self.vars = _vars
        
    def __str__(self):
        _vars = ''
        for v in self.vars:                
            _vars = _vars + ' ' + str(v)
        return "(" + self.operator + _vars + ")"
