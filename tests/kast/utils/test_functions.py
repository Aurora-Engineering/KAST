# GSC-19360-1, "Knowledge Acquisition and Synthesis Tool"
#
# Copyright © 2024 United States Government as represented by the 
# Administrator of the National Aeronautics and Space Administration.   
# All Rights Reserved.
#
# Licensed under the NASA Open Source Agreement version 1.3
# See "NOSA GSC-19360-1 KAST.pdf"

import pytest
from mock import MagicMock, PropertyMock
import importlib.util
import os

import kast.utils
from kast.utils.functions import import_module, get_attribute_by_name, extract_return_names
import kast
import kast.utils.functions

def test_import_module_throws_an_assertion_error_if_given_filepath_does_not_exist(mocker):
    # Arrange
    arg_name = MagicMock()
    arg_nonexistent_path = 'black_mage'

    # Act
    with pytest.raises(AssertionError) as einfo:
        import_module(module_name=arg_name,
                      file_to_import=arg_nonexistent_path)
        
    # Assert
    assert einfo.exconly() == f'AssertionError: File {arg_nonexistent_path} failed to import, check your config'

def test_import_module_does_not_throw_an_error_if_filepath_exists(mocker):
    # Arrange
    arg_name = MagicMock()
    arg_path = MagicMock()
    
    fake_spec = MagicMock()
    fake_module = MagicMock()

    mocker.patch('os.path.exists',return_value=True)
    mocker.patch('importlib.util.spec_from_file_location',return_value=fake_spec)
    mocker.patch('importlib.util.module_from_spec',return_value=fake_module)
    mocker.patch.object(fake_spec,'loader.exec_module')

    # Act
    import_module(module_name=arg_name,
                      file_to_import=arg_path)
        
    # Assert
    assert os.path.exists.call_count == 1


def test_import_module_runs_correct_series_of_importlib_functions(mocker):
    # Arrange
    arg_name = MagicMock()
    arg_file_to_import = MagicMock()

    fake_spec = MagicMock()
    fake_module = MagicMock()

    mocker.patch('importlib.util.spec_from_file_location',return_value=fake_spec)
    mocker.patch('importlib.util.module_from_spec',return_value=fake_module)
    mocker.patch.object(fake_spec,'loader.exec_module')

    # Act
    import_module(module_name=arg_name,
                  file_to_import=arg_file_to_import)

    # Assert
    assert importlib.util.spec_from_file_location.call_count == 1
    assert importlib.util.spec_from_file_location.call_args_list[0].args == (arg_name,arg_file_to_import)
    assert importlib.util.module_from_spec.call_count == 1
    assert importlib.util.module_from_spec.call_args_list[0].args == (fake_spec, )
    assert fake_spec.loader.exec_module.call_count == 1
    assert fake_spec.loader.exec_module.call_args_list[0].args == (fake_module, )

def test_get_attribute_by_name_calls_getattr(mocker):
    # Arrange
    fake_name = MagicMock()
    fake_module = MagicMock()
    fake_getattr = MagicMock()

    mocker.patch('kast.utils.functions.getattr',fake_getattr)

    # Act
    get_attribute_by_name(fake_module,fake_name)

    # Assert
    assert fake_getattr.call_count == 1


# test_extract_return_names...
def test_extract_return_names_calls_return_file_nodes_using_given_filepath(mocker):
    # Arrange
    fake_filepath = MagicMock()
    fake_function_name = MagicMock()

    mocker.patch('kast.utils.functions.return_file_nodes')

    # Act
    extract_return_names(fake_function_name, fake_filepath)

    # Assert
    assert kast.utils.functions.return_file_nodes.call_count == 1
    assert kast.utils.functions.return_file_nodes.call_args_list[0].args == (fake_filepath, )

def test_extract_return_names_skips_entries_that_are_not_function_definitions(mocker):
    # Arrange
    fake_filepath = MagicMock()
    fake_function_name = MagicMock()
    fake_name_attr = PropertyMock()


    fake_file_node = MagicMock(spec=1)
    type(fake_file_node).name = fake_name_attr

    mocker.patch('kast.utils.functions.return_file_nodes', return_value=[fake_file_node])
    mocker.patch.object(fake_file_node, 'name')

    # Act
    cut = extract_return_names(fake_function_name, fake_filepath)

    # Assert
    assert fake_file_node.name.call_count == 0
    assert cut == None

def test_extract_return_names_skips_entries_that_are_function_defs_but_do_not_match_the_given_function_name(mocker):
    # Arrange
    from ast import FunctionDef
    fake_filepath = MagicMock()
    fake_function_name = MagicMock()
    fake_name_attr = PropertyMock()
    fake_body_attr = PropertyMock()

    fake_file_node = MagicMock(spec=FunctionDef())
    type(fake_file_node).name = fake_name_attr
    type(fake_file_node).body = fake_body_attr

    mocker.patch('kast.utils.functions.return_file_nodes', return_value=[fake_file_node])

    # Act
    cut = extract_return_names(fake_function_name, fake_filepath)

    # Assert
    assert fake_name_attr.call_count == 1
    assert fake_body_attr.call_count == 0
    assert cut == None

def test_extract_return_names_calls_check_body_node_on_body_entries_with_return_from_body_attr(mocker):
    # Arrange
    from ast import FunctionDef
    fake_filepath = MagicMock()
    fake_function_name = MagicMock()
    fake_body_node = MagicMock()

    fake_name_attr = PropertyMock(return_value=fake_function_name)
    fake_body_attr = PropertyMock(return_value=[fake_body_node])

    fake_file_node = MagicMock(spec=FunctionDef())
    type(fake_file_node).name = fake_name_attr
    type(fake_file_node).body = fake_body_attr

    mocker.patch('kast.utils.functions.return_file_nodes', return_value=[fake_file_node])
    mocker.patch('kast.utils.functions.check_body_node', return_value=None)

    # Act
    cut = extract_return_names(fake_function_name, fake_filepath)

    # Assert
    assert kast.utils.functions.check_body_node.call_count == 1
    assert kast.utils.functions.check_body_node.call_args_list[0].args == (fake_body_node, )

def test_extract_return_names_returns_None_if_check_body_node_returns_None(mocker):
    # Arrange
    from ast import FunctionDef
    fake_filepath = MagicMock()
    fake_function_name = MagicMock()
    fake_body_node = MagicMock()

    fake_name_attr = PropertyMock(return_value=fake_function_name)
    fake_body_attr = PropertyMock(return_value=[fake_body_node])

    fake_file_node = MagicMock(spec=FunctionDef())
    type(fake_file_node).name = fake_name_attr
    type(fake_file_node).body = fake_body_attr

    mocker.patch('kast.utils.functions.return_file_nodes', return_value=[fake_file_node])
    mocker.patch('kast.utils.functions.check_body_node', return_value=None)

    # Act
    cut = extract_return_names(fake_function_name, fake_filepath)

    # Assert
    assert cut == None

def test_extract_return_names_returns_value_from_check_body_node_returns_if_check_body_node_returns_not_None(mocker):
    # Arrange
    from ast import FunctionDef
    fake_filepath = MagicMock()
    fake_function_name = MagicMock()
    fake_body_node = MagicMock()
    fake_overall_return = MagicMock()

    fake_name_attr = PropertyMock(return_value=fake_function_name)
    fake_body_attr = PropertyMock(return_value=[fake_body_node])

    fake_file_node = MagicMock(spec=FunctionDef())
    type(fake_file_node).name = fake_name_attr
    type(fake_file_node).body = fake_body_attr

    mocker.patch('kast.utils.functions.return_file_nodes', return_value=[fake_file_node])
    mocker.patch('kast.utils.functions.check_body_node', return_value=fake_overall_return)

    # Act
    cut = extract_return_names(fake_function_name, fake_filepath)

    # Assert
    assert cut == fake_overall_return