# Class to store knowledge (and possibly predicate) information, as well as methods to access and update that information
import sys

sys.path.append("..")

from typing import List, Dict, Tuple, Callable
from collections import namedtuple
from utils.parsers import *

from src.knowledge.core import Knowledge

Kaster = namedtuple('Kaster',['input_vars','output_vars','method'])

class Spellbook():
    def __init__(self,
                 low_level_headers: List[str], 
                 data_translation_methods: List[Tuple[str, str, callable]],
                 ) -> None:
        # Set internal vars
        

        # Initialize data structures
        self.low_level_knowledge = {}
        self.high_level_knowledge = {}
        self.kasters = []

        # Initialize functionality
        # self.init_parser() - need to consider more, maybe should stay in parser
        self.init_low_level_knowledge(low_level_headers)
        self.init_kasters(data_translation_methods)
        self.init_high_level_knowledge()

    def init_parser(self) -> None:
        raise NotImplementedError

    def init_low_level_knowledge(self, name_list: List[str]) -> None:
        # Generate low-level-knowledge objects for every item in name_list
        # (ex. one for every column in a dataframe)
        for name in name_list:
            self.low_level_knowledge[name] = Knowledge('low',name)

    def init_kasters(self, tuple_list: List[Tuple]) -> None:
        # Generate namedtuples of ways to go from high to low level knowledge
        for tuple in tuple_list:
            self.kasters.append(Kaster(tuple[0],tuple[1],tuple[2]))
    
    def init_high_level_knowledge(self) -> None:
        # Generate high-level-knowledge objects for every output variable defined in kasters
        for kaster in self.kasters:
            self.high_level_knowledge[kaster.output_vars] = Knowledge('high',kaster.output_vars)

    def update_low_level_knowledge(self,new_frame: Dict) -> None:
        # Update low-level-knowledge with new frame of data
        for name in new_frame.keys():
            self.low_level_knowledge[name].update(new_frame[name])

    def kast(self):
        # Use kasters to update high-level-knowledge, so long as the required input variables exist in the low-level-knowledge
        for kaster in self.kasters:
            if kaster.input_vars in self.low_level_knowledge.keys():
                # This is a doozy.
                # Set the high-level Knowledge item specified by the kaster output variable 
                # to the result of the translation function specified in the kaster method field
                # by calling that function using the value of the low-level Knowledge item specified by the kaster input variable
                # There's probably a ... cleaner way to do this
                self.high_level_knowledge[kaster.output_vars].update(kaster.method(self.low_level_knowledge[kaster.input_vars].value))