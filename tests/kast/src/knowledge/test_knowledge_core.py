import pytest
from mock import MagicMock
import numpy as np
import warnings

from kast.src.knowledge.core import Knowledge

def test_knowledge_core__init__sets_self_label_to_given_label(mocker):
    
    # Arrange
    cut = Knowledge.__new__(Knowledge)
    arg_label = MagicMock()

    # Action
    cut.__init__(arg_label,None,None)

    # Assert

    assert cut.label == arg_label

def test_knowledge_core__init__sets_self_name_to_given_name(mocker):
    
    # Arrange
    cut = Knowledge.__new__(Knowledge)
    arg_name = MagicMock()

    # Action
    cut.__init__(None,arg_name,None)

    # Assert

    assert cut.name == arg_name

def test_knowledge_core__init__sets_self_value_to_given_value(mocker):
    
    # Arrange
    cut = Knowledge.__new__(Knowledge)
    arg_value = MagicMock()

    # Action
    cut.__init__(None,None,arg_value)

    # Assert

    assert cut.value == arg_value

def test_knowledge_core__init__sets_self_type_to_type_of_given_value(mocker):
    
    # Arrange
    cut = Knowledge.__new__(Knowledge)
    arg_value = MagicMock()

    # Action
    cut.__init__(None,None,arg_value)

    # Assert
    assert cut._type == type(arg_value)

def test_knowledge_core__init__sets_value_and_type_to_none_and_nonetype_when_no_arg_value_given(mocker):
    # Arrange
    cut = Knowledge.__new__(Knowledge)

    # Action
    cut.__init__(None,None)

    # Assert
    assert cut.value == None
    assert cut._type == type(None)

def test_knowledge_core_update_throws_a_warning_when_changing_value_types(mocker):
    
    # Arrange
    arg_name = MagicMock()
    arg_value = 'string'
    update_value = 1.0

    cut = Knowledge(None,arg_name,arg_value)

    with warnings.catch_warnings(record=True) as w:
        # Act
        cut.update(update_value)

        # Assert
        assert len(w) == 1
        assert f"\n\tCaution: {cut.name} is being updated with new type; changing {type(arg_value)} to {type(update_value)}" in str(w[-1].message)

def test_knowledge_core_update_does_not_throw_a_warning_when_not_changing_value_types(mocker):

    # Arrange
    arg_name = MagicMock()
    arg_value = 'string'
    update_value = 'some_other_string'

    cut = Knowledge(None,arg_name,arg_value)

    with warnings.catch_warnings(record=True) as w:
        # Act
        cut.update(update_value)

        # Assert
        assert len(w) == 0

def test_knowledge_core_update_does_not_throw_a_warning_when_changing_value_type_away_from_none(mocker):

    # Arrange
    arg_name = MagicMock()
    update_value = 'string'

    cut = Knowledge(None,arg_name)

    with warnings.catch_warnings(record=True) as w:
        # Act
        cut.update(update_value)

        # Assert
        assert len(w) == 0

def test_knowledge_core__str__method_properly_returns_all_representative_info(mocker):

    # Arrange
    fake_name = MagicMock()
    fake_label = MagicMock()
    fake_value = MagicMock()
    fake__type = MagicMock()
    
    cut = Knowledge.__new__(Knowledge)
    cut.name = fake_name
    cut.label = fake_label
    cut.value = fake_value
    cut._type = fake__type

    # Act
    ret = cut.__str__()
    # Assert
    assert ret == f"({cut.name}: {cut.value} {cut._type})"


