#!/usr/bin/env python
from warnings import warn
from typing import Callable

class Knowledge(object):
    def __init__(self, _label: str, _name: str, _value=None):
        """
        Class representing a single datapoint of knowledge.

        Parameters
        ----------
        _label : str
            Is this knowledge low level (sub-symbolic) or high level (symbolic)?
        _name : str
            What does this knowledge represent? 
        _value : variable
            Information representing the knowledge
        """
        self.label = _label
        self.name = _name
        self.value = _value
        self._type = type(self.value)

        # When testing this function, write separate tests per *behavior* - i.e. test_label_is_set_to_label...
    
    def update(self,value):
        if type(value) != self._type and self._type != type(None):
            warn(f"\n\tCaution: {self.name} is being updated with new type; changing {self._type} to {type(value)}")
        self._type = type(value)
        self.value = value
        
    def __str__(self):
        return f"({self.name}: {self.value} {self._type} (Level: {self.label}))"
