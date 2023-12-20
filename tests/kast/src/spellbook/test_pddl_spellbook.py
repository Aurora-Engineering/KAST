import pytest
from mock import MagicMock, patch
import numpy as np
import warnings

from kast.src.spellbook.pddl_spellbook import *
from kast.src.knowledge.predicate import OPERATOR_MAPPINGS
from kast.src.knowledge.core import Knowledge

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

def test_init_predicates_updates_internal_dict_with_correctly_structured_predicates_(mocker):
    # Arrange
    
    num_fake_predicate_definitions = np.random.randint(1,10)

    fake_predicate_definitions = []

    for i in range(num_fake_predicate_definitions):
        op_mapping = np.random.randint(0,6)
        predicate_name = MagicMock()
        reference_variable = MagicMock()
        string_form_binary_operator = list(OPERATOR_MAPPINGS.keys())[op_mapping]
        numerical_value = MagicMock()

        definition_tuple = (predicate_name,
                            reference_variable,
                            string_form_binary_operator,
                            numerical_value
                            )

        fake_predicate_definitions.append(definition_tuple)

    cut = PDDLSpellbook.__new__(PDDLSpellbook)

    cut.predicates = {}

    # Act

    cut.init_predicates(fake_predicate_definitions)

    # Assert

    for (i, (key, value)) in enumerate(cut.predicates.items()):
        fake_predicate_indexed = fake_predicate_definitions[i]
        assert value.name == fake_predicate_indexed[0]
        assert value.reference_variable == fake_predicate_indexed[1]
        assert value.operator == OPERATOR_MAPPINGS[fake_predicate_indexed[2]]
        assert value.vars == fake_predicate_indexed[3]
        assert key == fake_predicate_indexed[0]
        
def test_evaluate_predicates_updates_all_predicates_based_on_operator_result_if_their_reference_variable_is_found_in_HLK(mocker):
    # Arrange
    num_fake_predicates = np.random.randint(1,10)
    fake_predicates_dict = {}
    fake_high_level_knowledge = {}

    fake_operator_results = []

    for i in range(num_fake_predicates):
        fake_predicate = MagicMock()
        fake_predicate.reference_variable = MagicMock()

        fake_knowledge = MagicMock()

        forced_predicate_result = bool(np.random.randint(0,2))
        fake_operator_results.append(forced_predicate_result)

        mocker.patch.object(fake_predicate,'operator',return_value=forced_predicate_result)
         
        fake_predicates_dict.update({i:fake_predicate})
        fake_high_level_knowledge.update({fake_predicate.reference_variable: fake_knowledge})


    cut = PDDLSpellbook.__new__(PDDLSpellbook)
    cut.high_level_knowledge = fake_high_level_knowledge
    cut.predicates = fake_predicates_dict
    cut.state = {}

    # Act
    cut.evaluate_predicates()

    # Assert
    assert len(cut.state) == num_fake_predicates

    for i in range(num_fake_predicates):
        assert fake_predicates_dict[i].operator.call_count == 1
        assert cut.state[fake_predicates_dict[i].name] == fake_operator_results[i]
    
def test_evaluate_predicates_throws_error_if_reference_variable_is_not_found_in_high_level_knowledge(mocker):
        # Arrange
    num_fake_predicates = np.random.randint(1,10)
    fake_predicates_dict = {}
    fake_high_level_knowledge = {}

    fake_operator_results = []

    for i in range(num_fake_predicates):
        fake_predicate = MagicMock()
        fake_predicate.reference_variable = MagicMock()

        fake_knowledge = MagicMock()

        forced_predicate_result = bool(np.random.randint(0,2))
        fake_operator_results.append(forced_predicate_result)

        mocker.patch.object(fake_predicate,'operator',return_value=forced_predicate_result)

        fake_predicates_dict.update({i:fake_predicate})
        fake_high_level_knowledge.update({fake_predicate.reference_variable: fake_knowledge})

    excluded_fake_predicate = MagicMock()
    excluded_fake_predicate.name = MagicMock()
    excluded_fake_predicate.reference_variable = 'this_is_not_included'
    fake_predicates_dict.update({num_fake_predicates:excluded_fake_predicate})

    cut = PDDLSpellbook.__new__(PDDLSpellbook)
    cut.high_level_knowledge = fake_high_level_knowledge
    cut.predicates = fake_predicates_dict
    cut.state = {}

    # Act
    with pytest.warns() as w_info:
        cut.evaluate_predicates()

    # Assert

    for i in range(num_fake_predicates):
        assert fake_predicates_dict[i].operator.call_count == 1
        assert cut.state[fake_predicates_dict[i].name] == fake_operator_results[i]
    
    print((w_info.list[0].message))
    assert len(w_info) == 1
    assert str(w_info[0].message) == f"\n\t>>Warning! {excluded_fake_predicate.name} cannot find {excluded_fake_predicate.reference_variable} in high level knowledge."
