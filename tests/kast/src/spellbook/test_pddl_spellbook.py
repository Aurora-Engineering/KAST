import pytest
from mock import MagicMock, patch
import numpy as np
import warnings

from kast.src.spellbook.pddl_spellbook import *
from kast.src.knowledge.predicate import OPERATOR_MAPPINGS
from kast.src.knowledge.core import Knowledge

import kast.src.knowledge.predicate as predicate_file

def test__init__calls_super_init_initializes_predicates_and_calls_init_predicates(mocker):
    
    # Arrange
    mocker.patch.object(Spellbook,'__init__')
    cut = PDDLSpellbook.__new__(PDDLSpellbook)

    fake_low_level_headers = MagicMock()
    fake_data_translation_methods = MagicMock()
    fake_predicate_definitions = MagicMock()

    mocker.patch.object(cut,'init_predicates')
    

    # Action
    cut.__init__(fake_low_level_headers,fake_data_translation_methods,fake_predicate_definitions)

    # Assert

    assert Spellbook.__init__.call_count == 1
    assert cut.init_predicates.call_count == 1

def test_init_predicates_updates_internal_dict_with_correctly_structured_predicates_from_arguments(mocker):
    # Arrange
    
    num_fake_predicate_definitions = np.random.randint(1,10)

    arg_predicate_definitions = []

    for i in range(num_fake_predicate_definitions):
        predicate_name = MagicMock()
        reference_variables_list = MagicMock()
        string_form_binary_operators_list = MagicMock()
        numerical_value_list = MagicMock()

        definition_tuple = (predicate_name,
                            reference_variables_list,
                            string_form_binary_operators_list,
                            numerical_value_list
                            )

        arg_predicate_definitions.append(definition_tuple)

    cut = PDDLSpellbook.__new__(PDDLSpellbook)

    cut.predicates = {}

    mocker.patch(predicate_file.__name__ + '.Predicate.__init__',return_value=None)

    # Act

    cut.init_predicates(arg_predicate_definitions)

    # Assert
    assert predicate_file.Predicate.__init__.call_count == num_fake_predicate_definitions
    for arg_tuple in arg_predicate_definitions:
        predicate_file.Predicate.__init__.assert_any_call(arg_tuple[0],arg_tuple[1],arg_tuple[2],arg_tuple[3])
        
def test_evaluate_predicates_updates_predicates_based_on_operators_for_each_listed_reference_variable_if_their_required_reference_variables_are_available_in_high_level_knowledge(mocker):
    # Arrange
    num_fake_predicates = np.random.randint(1,10)

    fake_predicates = {}
    fake_high_level_knowledge = {}
    
    for i in range(num_fake_predicates):
        fake_predicate = MagicMock()
        fake_name = MagicMock()
        fake_ref_vars = [MagicMock() for i in range(num_fake_predicates)]
        fake_operators = [MagicMock(return_value=np.random.randint(0,2)) for i in range(num_fake_predicates)]
        fake_expected_vars = [MagicMock() for i in range(num_fake_predicates)]

        for ref_var in fake_ref_vars:
            fake_high_level_knowledge.update({ref_var: MagicMock()})
        


        fake_predicate.name = fake_name
        fake_predicate.reference_variable = fake_ref_vars
        fake_predicate.operator = fake_operators
        fake_predicate.vars = fake_expected_vars

        fake_predicates.update({fake_name: fake_predicate})
        fake_high_level_knowledge.update({fake_name: MagicMock()}) # HLK needs to have entries for all ref_vars

    cut = PDDLSpellbook.__new__(PDDLSpellbook)

    cut.predicates = fake_predicates
    cut.high_level_knowledge = fake_high_level_knowledge

    # Act
    cut.evaluate_predicates()

    # Assert
    assert len(cut.state.keys()) == num_fake_predicates
    assert all(isinstance(x, int) for x in cut.state.values())

    for i, (key, value) in enumerate(cut.predicates.items()):
        predicate = value
        for i, operator in enumerate(predicate.operator):
            reference_variable = predicate.reference_variable[i]
            reference_variable_value = cut.high_level_knowledge[reference_variable].value
            predicate_expectation = predicate.vars[i]
            
            operator.assert_called_once_with(reference_variable_value,predicate_expectation)

### DEPRECATED - going to move this functionality out of evaluate_predicates with issue #10
# def test_evaluate_predicates_throws_error_if_reference_variable_is_not_found_in_high_level_knowledge(mocker):
#     # Arrange
#     num_fake_predicates = np.random.randint(1,10)
#     fake_predicates_dict = {}
#     fake_high_level_knowledge = {}

#     fake_operator_results = []

#     for i in range(num_fake_predicates):
#         fake_predicate = MagicMock()
#         fake_predicate.reference_variable = MagicMock()

#         fake_knowledge = MagicMock()

#         forced_predicate_result = bool(np.random.randint(0,2))
#         fake_operator_results.append(forced_predicate_result)

#         mocker.patch.object(fake_predicate,'operator',return_value=forced_predicate_result)

#         fake_predicates_dict.update({i:fake_predicate})
#         fake_high_level_knowledge.update({fake_predicate.reference_variable: fake_knowledge})

#     excluded_fake_predicate = MagicMock()
#     excluded_fake_predicate.name = MagicMock()
#     excluded_fake_predicate.reference_variable = 'this_is_not_included'
#     fake_predicates_dict.update({num_fake_predicates:excluded_fake_predicate})

#     cut = PDDLSpellbook.__new__(PDDLSpellbook)
#     cut.high_level_knowledge = fake_high_level_knowledge
#     cut.predicates = fake_predicates_dict
#     cut.state = {}

#     # Act
#     with pytest.warns() as w_info:
#         cut.evaluate_predicates()

#     # Assert

#     for i in range(num_fake_predicates):
#         for operator_callable
#         assert fake_predicates_dict[i].operator.call_count == 1
#         assert cut.state[fake_predicates_dict[i].name] == fake_operator_results[i]
    
#     print((w_info.list[0].message))
#     assert len(w_info) == 1
#     assert str(w_info[0].message) == f"\n\t>>Warning! {excluded_fake_predicate.name} cannot find {excluded_fake_predicate.reference_variable} in high level knowledge."
