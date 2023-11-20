# Subclass of Spellbook to use for PDDL specific, featuring predicate generation and storing
from typing import List, Dict, Tuple, Callable, Any
import operator as op
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
    
    def binary_operator_predicate(self,reference_variable: str, str_binary_operator: str, numerical_val: List, predicate_name: str):
        """
        Convert SME input on predicate using binary operator comparison into Predicate class

        Parameters
        ----------
        reference_variable : str
            What variable does the predicate depend on?
        str_binary_operator : str
            What operator (<, !=, >=, etc) does the predicate use to compare the current value to the reference value?
        numerical_val : List
            What are the reference numerical values to compare readings to?
        predicate_name : str
            What quality does the predicate describe?
        """
        op_mappings = {'<': op.lt, # Create a mapping of string reps of comparison operators to functions to make these attributes evaluatable
                    '<=': op.le,
                    '==': op.eq,
                    '!=': op.ne,
                    '>': op.gt,
                    '>=': op.lt}
        binary_operator = op_mappings[str_binary_operator]
        pred = Predicate(predicate_name,reference_variable,binary_operator,numerical_val)
        
        return({predicate_name: pred})
    
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

            self.predicates.update(self.binary_operator_predicate(ref_var,s_bin_op,num_val,pred_name))

    def evaluate_predicates(self):
        """
        Loops through internally stored predicates, comparing to current high level data to get state information
        """
        temp_state = {} # Update name
        for predicate in self.predicates.values(): 
            if predicate.reference_variable in self.high_level_knowledge.keys():
                temp_state.update(
                    {predicate.name: predicate.operator(self.high_level_knowledge[predicate.reference_variable].value, predicate.vars)}
                    )
            else: # Raise an error if some predicate is not being captured in high level data
                warn(f"\n\t>>Warning! {predicate.name} cannot find {predicate.reference_variable} in high level knowledge.")

        self.state: Dict[str, bool] = temp_state
