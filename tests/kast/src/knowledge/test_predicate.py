import pytest
from mock import MagicMock
import numpy as np

import kast.src.knowledge.predicate as predicate_file
from kast.src.knowledge.predicate import *

def test_get_binary_op_mappings_returns_list_of_operator_instances_when_given_string_representations(mocker):
    # Arrange
    num_operators = np.random.randint(1,10)
    arg_operator_strings_list = []
    for i in range(num_operators):
        random_key_index = np.random.randint(0,5)
        operator_string = list(OPERATOR_MAPPINGS.keys())[random_key_index]
        arg_operator_strings_list.append(operator_string)

    # Act
    cut = get_binary_op_mappings(arg_operator_strings_list)

    # Assert
    len(cut) == num_operators
    for i, operator in enumerate(cut):
        operator == OPERATOR_MAPPINGS[arg_operator_strings_list[i]]

def test_get_binary_op_mappings_throws_an_error_when_given_an_incorrect_operator_key(mocker):
    # Arrange
    random_key_index = np.random.randint(0,5)
    good_operator_string = list(OPERATOR_MAPPINGS.keys())[random_key_index]
    bad_operator_string = MagicMock()
    
    # Act
    with pytest.raises(KeyError) as e_info:
        get_binary_op_mappings(['<',bad_operator_string])
    
    # Assert
    assert f'Given operator {bad_operator_string} is not contained in the binary operator mappings list. Check syntax.' in e_info.exconly()


def test_predicate__init__sets_self_name_to_given_name():
    # Arrange
    cut = Predicate.__new__(Predicate)
    arg_name = MagicMock()
    placeholder_operator = '>'

    # Act
    cut.__init__(arg_name, None, placeholder_operator, None)

    # Assert
    assert cut.name == arg_name

def test_predicate__init__sets_self_reference_variable_to_given_reference_variable():
    # Arrange
    cut = Predicate.__new__(Predicate)
    arg_ref_var = MagicMock()
    placeholder_operator = '>'

    # Act
    cut.__init__(None,arg_ref_var, placeholder_operator, None)

    # Assert
    assert cut.reference_variable == arg_ref_var

def test_predicate__init__sets_self_operator_to_given_operator_by_calling_get_binary_op_mappings(mocker):
    # Arrange
    cut = Predicate.__new__(Predicate)
    arg_operator_strings_list = MagicMock()
    forced_return_value = MagicMock()

    mocker.patch(predicate_file.__name__ + '.get_binary_op_mappings',return_value=forced_return_value)

    # Act
    cut.__init__(None, None, arg_operator_strings_list, None)

    # Assert
    predicate_file.get_binary_op_mappings.assert_called_once_with(arg_operator_strings_list)
    assert cut.operator == forced_return_value


def test_predicate__init__sets_self_vars_to_given_vars():
    # Arrange
    cut = Predicate.__new__(Predicate)
    arg_vars = MagicMock()
    placeholder_operator = '>'

    # Act
    cut.__init__(None, None, placeholder_operator, arg_vars)

    # Assert
    assert cut.vars == arg_vars


def test_knowledge_core__str__method_properly_returns_all_representative_info(mocker):

    # Arrange
    fake_name = MagicMock()
    fake_reference_variable = MagicMock()
    fake_vars = MagicMock()
    fake_operator = MagicMock()
    fake_operator.__name__ = MagicMock()

    cut = Predicate.__new__(Predicate)
    cut.name = fake_name
    cut.reference_variable = fake_reference_variable
    cut.operator = fake_operator
    cut.vars = fake_vars

    # Act
    ret = cut.__str__()

    # Assert
    assert ret == f'({fake_name}: {fake_reference_variable} {fake_operator.__name__} {fake_vars})'
