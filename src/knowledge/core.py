#!/usr/bin/env python
from warnings import warn

class Knowledge(object):
    def __init__(self, _label: str, _name: str, _value, _type):
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
        _type : variable
            What Python class is this knowledge an instance of?
        """
        self.label = _label 
        self.name = _name       
        self.type = _type
        self.value = _value

    def get_value(self):
        return(self.value)

    def get_type(self):
        return(self.type)
    
    def get_name(self):
        return(self.name)
    
    def update(self,value):
        if type(value) != self.type:
            warn(f"\n\tCaution: {self.name} is being updated with new type; changing {self.type} to {type(value)}")
        self.type = type(value)
        self.value = value
    
    def __str__(self):
        return f"({self.name}: {self.value} {self.type} (Level: {self.label}))"
