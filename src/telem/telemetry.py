#!/usr/bin/env python

class Telemetry(object):
    def __init__(self, _label: str, _value, _type):
        self.label = _label
        self.type = _type
        self.value = _value

    def get_value(self):
        return(self.value)

    def get_type(self):
        return(self.type)
        
    def __str__(self):
        return f"({self.label}: {self.value} {self.type})"
