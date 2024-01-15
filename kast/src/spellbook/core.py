# Class to store knowledge (and possibly predicate) information, as well as methods to access and update that information
from typing import List, Dict, Tuple, Callable

from kast.utils.parsers import *
from kast.src.knowledge.core import Knowledge

class Kaster():
    def __init__(self,
                 input_vars: List[str],
                 output_vars: List[str],
                 method: Callable
                 ):
        self.input_vars = input_vars
        self.output_vars = output_vars
        self.method = method
 
class Spellbook():
    def __init__(self,
                 low_level_headers: List[str], 
                 data_translation_methods: List[Tuple[str, str, Callable]],
                 ) -> None:

        # Initialize data structures
        self.low_level_knowledge: Dict[str, Knowledge] = {}
        self.high_level_knowledge: Dict[str, Knowledge] = {}
        self.kasters: List[Kaster] = []

        # Initialize functionality
        # self.init_parser() - need to consider more, maybe should stay in parser
        self.init_low_level_knowledge(low_level_headers)
        self.init_kasters(data_translation_methods)
        self.init_high_level_knowledge()

    def init_low_level_knowledge(self, name_list: List[str]) -> None:
        # Generate low-level-knowledge objects for every item in name_list
        # (ex. one for every column in a dataframe)
        for name in name_list:
            self.low_level_knowledge[name] = Knowledge('low',name)

    def init_kasters(self, tuple_list: List[Tuple]) -> None:
        # Generate namedtuples of ways to go from high to low level knowledge
        available_low_level_knowledge = self.low_level_knowledge.keys()
        for tuple_entry in tuple_list:
            required_input = tuple_entry[0]
            if set(required_input).issubset(set(available_low_level_knowledge)):
                self.kasters.append(Kaster(tuple_entry[0],tuple_entry[1],tuple_entry[2]))
            else:
                raise KeyError(f'Kaster input variable {required_input} was not found in the available low level knowledge.')
    
    def init_high_level_knowledge(self) -> None:
        # Generate high-level-knowledge objects for every output variable defined in kasters
        for kaster in self.kasters:
            for output_variable in kaster.output_vars:
                self.high_level_knowledge[output_variable] = Knowledge('high',output_variable)

    def update_low_level_knowledge(self,new_frame: Dict) -> None:
        # Update low-level-knowledge with new frame of data
        for name in new_frame.keys():
            if name not in self.low_level_knowledge.keys(): # If presented with an unseen piece of knowledge, create a new low-level representation
                self.low_level_knowledge[name] = Knowledge('low',name,new_frame[name])
            self.low_level_knowledge[name].update(new_frame[name])

    def kast(self) -> None:
        for kaster in self.kasters:
            # Create dictionary of {'input_var_name': value from low_level_knowledge}
            input_variables = dict([(variable, self.low_level_knowledge[variable].value) for variable in kaster.input_vars])
            returned_knowledge = kaster.method(**input_variables) # Unpack above dictionary as kwargs for kasting method
            # Assuming that returned values will be a dictionary of {'output_var': value}
            # Can we mandate a function return a dictionary of output variables? Will need to standardize somehow; is there a generalized method for handling this beyond the dictionary?
            for output_variable_name in returned_knowledge.keys():
                self.high_level_knowledge[output_variable_name].update(returned_knowledge[output_variable_name]) # Update high_level_knowedge entries with corresponding return values
