# Subclass of Spellbook to use for PDDL specific, featuring predicate generation and storing
from typing import List, Dict, Tuple, Callable, Any
from warnings import warn

from .core import Spellbook
from ..knowledge.predicate import Predicate



class PDDLSpellbook(Spellbook):
    def __init__(self, 
                 low_level_headers: List[str], 
                 data_translation_methods: List[Tuple[str, str, Callable]],
                 predicate_definitions: List[Tuple[str,str,str]]):
        super().__init__(low_level_headers, data_translation_methods)

        self.predicates: Dict[str, Predicate] = {}
        
        self.init_predicates(predicate_definitions)
    
    def init_predicates(self, predicate_definitions: List[Tuple[str,str,Any]]):
        """
        Initialize list of predicates

        Currently only encompasses binary comparison but should eventually be expanded to other methods

        Parameters
        ----------
        predicate_definitions : List[Tuple[str,str,Any]]
            _description_
        """
        for predicate_tuple in predicate_definitions:
            pred_name = predicate_tuple[0]
            ref_var = predicate_tuple[1]
            s_bin_op = predicate_tuple[2]
            num_val = predicate_tuple[3]

            labeled_predicate = {pred_name: Predicate(pred_name,ref_var,s_bin_op,num_val)}

            self.predicates.update(labeled_predicate)

    def evaluate_predicates(self):
        """
        Loops through internally stored predicates, comparing to current high level data to get state information
        """
        temp_state = {} # Update name
        for predicate in self.predicates.values(): 
            if predicate.reference_variable in self.high_level_knowledge.keys():
                reference_var_current_value = self.high_level_knowledge[predicate.reference_variable].value
                predicate_expectation = predicate.vars
                temp_state.update(
                    {predicate.name: predicate.operator(reference_var_current_value, predicate_expectation)}
                    )
            else: # Raise an error if some predicate is not being captured in high level data
                warn(f"\n\t>>Warning! {predicate.name} cannot find {predicate.reference_variable} in high level knowledge.")

        self.state: Dict[str, bool] = temp_state
