# GSC-19360-1, "Knowledge Acquisition and Synthesis Tool"
#
# Copyright © 2024 United States Government as represented by the 
# Administrator of the National Aeronautics and Space Administration.   
# All Rights Reserved.
#
# Licensed under the NASA Open Source Agreement version 1.3
# See "NOSA GSC-19360-1 KAST.pdf"

import pytest
import mock
from mock import MagicMock

import os
import configparser
from inspect import isfunction

import kast
import kast.src
from kast.src.kast_runtime import *
import kast.src.kast_runtime
from kast.src.spellbook import Spellbook


def test_runtime_core__init__sets_internal_filepath_to_given_arg_filepath(mocker):
    # Arrange
    cut = KastRuntime.__new__(KastRuntime)
    arg_filepath = MagicMock()

    cut.data_source = MagicMock()
    cut.kaster_definitions = MagicMock()
    cut.headers = MagicMock()

    mocker.patch.object(cut,'parse_config')
    mocker.patch.object(cut,'import_kaster_methods')
    mocker.patch.object(cut,'initialize_data_source')

    # Action
    cut.__init__(arg_filepath)

    # Assert

    assert cut._config_filepath == arg_filepath

def test_runtime_core__init__raises_assertion_error_if_given_path_does_not_exist(mocker):
    # Arrange

    fake_file_path = MagicMock()

    cut = KastRuntime.__new__(KastRuntime)
    mocker.patch('os.path.exists',return_value=False)

    # Act
    with pytest.raises(AssertionError) as einfo:
        cut.__init__(fake_file_path)

    # Assert
    assert os.path.exists.call_count == 1
    assert os.path.exists.call_args_list[0].args == (fake_file_path,)
    assert einfo.exconly() == f'AssertionError: Specified config filepath {cut._config_filepath} cannot be found.'

def test_runtime_core__init__does_not_raise_assertion_error_if_given_path_exists(mocker):
    # Arrange
    fake_file_path = MagicMock()

    cut = KastRuntime.__new__(KastRuntime)
    cut.data_source = MagicMock()
    cut.kaster_definitions = MagicMock()
    cut.headers = MagicMock()

    mocker.patch('os.path.exists',return_value=True)
    mocker.patch.object(cut,'parse_config')
    mocker.patch.object(cut,'import_kaster_methods')
    mocker.patch.object(cut,'initialize_data_source')

    # Act
    cut.__init__(fake_file_path)

    # Assert
    assert os.path.exists.call_count == 1
    assert os.path.exists.call_args_list[0].args == (fake_file_path,)

def test_runtime_core__init__calls_expected_initialization_methods(mocker):
    
    # Arrange
    cut = KastRuntime.__new__(KastRuntime)
    arg_filepath = MagicMock()

    cut.data_source = MagicMock()
    cut.kaster_definitions = MagicMock()
    cut.headers = MagicMock()

    mocker.patch.object(cut,'parse_config')
    mocker.patch.object(cut,'import_kaster_methods')
    mocker.patch.object(cut,'initialize_data_source')

    # Action
    cut.__init__(arg_filepath)

    # Assert

    assert cut.parse_config.call_count == 1
    assert cut.import_kaster_methods.call_count == 1
    assert cut.initialize_data_source.call_count == 1

def test_runtime_core__init__generates_attribute_spellbook_with_internal_headers_and_kasters(mocker):
    # Arrange

    cut = KastRuntime.__new__(KastRuntime)
    arg_filepath = MagicMock()
    fake_data_source = MagicMock()
    fake_kaster_definitions = MagicMock()
    fake_headers = MagicMock()

    cut.data_source = fake_data_source
    cut.kaster_definitions = fake_kaster_definitions
    cut.headers = fake_headers

    mocker.patch.object(cut,'parse_config')
    mocker.patch.object(cut,'import_kaster_methods')
    mocker.patch.object(cut,'initialize_data_source')
    mocker.patch('kast.src.kast_runtime.Spellbook.__init__',return_value=None)

    # Action
    cut.__init__(arg_filepath)

    # Assert
    assert type(cut.spellbook) == Spellbook
    assert cut.spellbook.__init__.call_count == 1
    assert cut.spellbook.__init__.call_args_list[0].args == (fake_headers,fake_kaster_definitions)

def test_runtime_core_parse_config_generates_config_reader_and_reads_given_file(mocker):
    # Arrange 
    fake_config_filepath = MagicMock()
    fake_config = MagicMock()
    fake_config_dict = {'DEFAULT':{
                        'KasterMethodsPath': MagicMock(),
                        'DataFile': MagicMock(),
                        'DataType': MagicMock()
        }
    }
    fake_config.__getitem__.side_effect = fake_config_dict.__getitem__
    

    cut = KastRuntime.__new__(KastRuntime)
    cut._config_filepath = fake_config_filepath

    mocker.patch('configparser.ConfigParser.__init__')
    mocker.patch('configparser.ConfigParser',return_value=fake_config)
    mocker.patch.object(fake_config,'read',return_value=None)

    # Act
    cut.parse_config()

    # Assert
    assert configparser.ConfigParser.call_count == 1
    assert cut.config == fake_config
    assert fake_config.read.call_count == 1
    assert fake_config.read.call_args_list[0].args == (fake_config_filepath, )


def test_runtime_core_parse_config_sets_correct_internal_references_from_given_config(mocker):
    # Arrange
    fake_config_filepath = MagicMock()
    fake_config = MagicMock()
    fake_config_dict = {'DEFAULT':{
                        'KasterMethodsPath': MagicMock(),
                        'DataFile': MagicMock(),
                        'DataType': MagicMock()
        }
    }
    fake_config.__getitem__.side_effect = fake_config_dict.__getitem__
    

    cut = KastRuntime.__new__(KastRuntime)
    cut._config_filepath = fake_config_filepath

    mocker.patch('configparser.ConfigParser.__init__')
    mocker.patch('configparser.ConfigParser',return_value=fake_config)
    mocker.patch.object(fake_config,'read',return_value=None)

    # Act
    cut.parse_config()

    # Assert
    assert cut.kaster_methods_path == fake_config_dict['DEFAULT']['KasterMethodsPath']
    assert cut.data_file_path == fake_config_dict['DEFAULT']['DataFile']
    assert cut.data_type == fake_config_dict['DEFAULT']['DataType']

def test_runtime_core_import_kaster_methods_initializes_headers_and_kaster_definitions_as_empty_lists(mocker):

    # Arrange
    cut = KastRuntime.__new__(KastRuntime)
    cut.kaster_methods_path = MagicMock()

    mocker.patch('kast.src.kast_runtime.import_module', side_effect=Exception('short-circuit summoner'))

    # Act
    with pytest.raises(Exception) as einfo:
        cut.import_kaster_methods()

    # Assert
    assert einfo.exconly() == 'Exception: short-circuit summoner'
    assert cut.headers == []
    assert cut.kaster_definitions == []

def test_runtime_core_import_kaster_methods_calls_import_module_using_attr_kaster_methods_path(mocker):

    # Arrange
    fake_kaster_methods_path = MagicMock()

    cut = KastRuntime.__new__(KastRuntime)
    cut.kaster_methods_path = fake_kaster_methods_path

    mocker.patch('kast.src.kast_runtime.getmembers', side_effect=Exception('short-circuit red mage'))
    mocker.patch('kast.src.kast_runtime.import_module')
    
    # Act
    with pytest.raises(Exception) as einfo:
        cut.import_kaster_methods()

    # Assert
    assert einfo.exconly() == 'Exception: short-circuit red mage'
    assert kast.src.kast_runtime.import_module.call_count == 1
    assert kast.src.kast_runtime.import_module.call_args_list[0].kwargs == {'module_name':'kaster_methods','file_to_import': fake_kaster_methods_path}

def test_runtime_core_import_kaster_methods_calls_getmembers_using_import_module_output_and_isfunction(mocker):

    # Arrange
    fake_module = MagicMock()
    
    cut = KastRuntime.__new__(KastRuntime)
    cut.kaster_methods_path = MagicMock()

    mocker.patch('kast.src.kast_runtime.import_module', return_value=fake_module)
    mocker.patch('kast.src.kast_runtime.getmembers', side_effect=Exception('short-circuit dark knight'))
    
    # Act
    with pytest.raises(Exception) as einfo:
        cut.import_kaster_methods()

    # Assert
    assert einfo.exconly() == 'Exception: short-circuit dark knight'
    assert kast.src.kast_runtime.getmembers.call_count == 1
    assert kast.src.kast_runtime.getmembers.call_args_list[0].args == (fake_module, isfunction)

def test_runtime_core_import_kaster_methods_creates_input_and_output_variables_with_correct_call_sequence(mocker):
    
    # Arrange
    num_fake_functions = pytest.gen.randint(0,10)
    fake_function_tuple_list = []
    cut = KastRuntime.__new__(KastRuntime)

    fake_module = MagicMock()
    fake_kaster_methods_path = MagicMock()

    cut.kaster_methods_path = fake_kaster_methods_path
    cut.kaster_definitions = MagicMock()

    for i in range(num_fake_functions):
        fake_tuple = (MagicMock(), MagicMock()) # (function_name, function_callable)
        fake_function_tuple_list.append(fake_tuple)
    
    mocker.patch('kast.src.kast_runtime.import_module', return_value=fake_module)
    mocker.patch('kast.src.kast_runtime.getmembers', return_value=fake_function_tuple_list)
    mocker.patch('kast.src.kast_runtime.getfullargspec')
    mocker.patch('kast.src.kast_runtime.extract_return_names')
    
    # Act
    cut.import_kaster_methods()

    # Assert
    assert kast.src.kast_runtime.getfullargspec.call_count == num_fake_functions
    assert kast.src.kast_runtime.extract_return_names.call_count == num_fake_functions
    for index, f in enumerate(fake_function_tuple_list):
        assert kast.src.kast_runtime.getfullargspec.call_args_list[index].args == (f[1], )
        assert kast.src.kast_runtime.extract_return_names.call_args_list[index].args == (f[0], fake_kaster_methods_path)

# 

def test_runtime_core_import_kaster_methods_sets_kaster_definitions_to_returns_from_fullargspec_and_extract_return_names_and_callable_function(mocker):
    
    # Arrange
    num_fake_functions = pytest.gen.randint(0,10)
    fake_function_tuple_list = []
    fake_input_var_list = []
    fake_output_var_list = []
    cut = KastRuntime.__new__(KastRuntime)

    fake_module = MagicMock()
    fake_kaster_methods_path = MagicMock()

    cut.kaster_methods_path = fake_kaster_methods_path
    cut.kaster_definitions = MagicMock()

    for i in range(num_fake_functions):
        fake_input_var = MagicMock()
        fake_output_var = MagicMock()
        fake_tuple = (MagicMock(), MagicMock()) # (function_name, function_callable)

        fake_input_var_list.append(fake_input_var)
        fake_output_var_list.append(fake_output_var)
        fake_function_tuple_list.append(fake_tuple)
    
    mocker.patch('kast.src.kast_runtime.import_module', return_value=fake_module)
    mocker.patch('kast.src.kast_runtime.getmembers', return_value=fake_function_tuple_list)
    mocker.patch('kast.src.kast_runtime.getfullargspec', side_effect=fake_input_var_list)
    mocker.patch('kast.src.kast_runtime.extract_return_names', side_effect=fake_output_var_list)
    
    # Act
    cut.import_kaster_methods()

    # Assert
    assert len(cut.kaster_definitions) == num_fake_functions
    for index, f in enumerate(fake_function_tuple_list):
        assert cut.kaster_definitions[index] == (fake_input_var_list[index].args, fake_output_var_list[index], f[1])
# sets_headers_to_return_from_fullargspec

def test_runtime_core_import_kaster_methods_sets_headers_to_return_from_fullargspec_by_iteration(mocker):
    
    # Arrange
    num_fake_functions = pytest.gen.randint(0,10)
    num_fake_input_vars = pytest.gen.randint(1,10)
    fake_function_tuple_list = []
    fake_argspec_returns_list = []
    cut = KastRuntime.__new__(KastRuntime)

    fake_module = MagicMock()
    fake_kaster_methods_path = MagicMock()

    cut.kaster_methods_path = fake_kaster_methods_path

    ### FIX: need getfullargspec return to be able to be referenced with .args (check the code)

    for i in range(num_fake_functions):
        fake_input_vars = [MagicMock() for i in range(num_fake_input_vars)]
        fake_argspec_return = MagicMock(args=fake_input_vars)
        fake_tuple = (fake_input_vars, MagicMock()) # (function_name, function_callable)

        fake_argspec_returns_list.append(fake_argspec_return)
        fake_function_tuple_list.append(fake_tuple)
    
    mocker.patch('kast.src.kast_runtime.import_module', return_value=fake_module)
    mocker.patch('kast.src.kast_runtime.getmembers', return_value=fake_function_tuple_list)
    mocker.patch('kast.src.kast_runtime.getfullargspec', side_effect=fake_argspec_returns_list)
    mocker.patch('kast.src.kast_runtime.extract_return_names')
    
    # Act
    cut.import_kaster_methods()

    # Assert
    assert len(cut.headers) == num_fake_input_vars*num_fake_functions
    for i in range(len(fake_argspec_returns_list)):
        assert set(fake_argspec_returns_list[i].args).issubset(set(cut.headers))
    
def test_runtime_core_initialize_data_source_imports_datatype_specified_data_source_using_importmodule_then_sets_internal_data_source_to_instance_of_imported_class(mocker):
    # Arrange
    fake_data_type = MagicMock()
    fake_module = MagicMock()
    fake_class_reference = MagicMock()

    cut = KastRuntime.__new__(KastRuntime)
    cut.data_type = fake_data_type

    mocker.patch('kast.src.kast_runtime.import_module',return_value=fake_module)
    mocker.patch('kast.src.kast_runtime.get_attribute_by_name',return_value=fake_class_reference)
    
    # Act
    cut.initialize_data_source()

    # Assert
    assert kast.src.kast_runtime.import_module.call_count == 1
    assert kast.src.kast_runtime.import_module.call_args_list[0].kwargs == {'module_name': 'data_source', 'file_to_import': f'kast/utils/data_sources/{cut.data_type}_data_source.py'}
    assert kast.src.kast_runtime.get_attribute_by_name.call_count == 1
    assert kast.src.kast_runtime.get_attribute_by_name.call_args_list[0].args == (fake_module,f'{cut.data_type.title()}DataSource')
    assert fake_class_reference.call_count == 1
    assert fake_class_reference.call_args_list[0].args == (cut, )
    assert cut.data_source == fake_class_reference()

def test_runtime_core_run_step_queries_data_source_if_override_is_not_given(mocker):
    # Arrange
    fake_low_level_information = MagicMock()

    cut = KastRuntime.__new__(KastRuntime)
    cut.data_source = MagicMock()
    cut.spellbook = MagicMock()
    
    mocker.patch.object(cut.data_source,'get_new_information',return_value=fake_low_level_information)
    mocker.patch.object(cut.spellbook, 'update_low_level_knowledge',side_effect=Exception('short_circuit_white_mage'))

    # Act
    with pytest.raises(Exception) as einfo:
        cut.run_step()

    # Assert
    assert einfo.exconly() == 'Exception: short_circuit_white_mage'
    assert cut.data_source.get_new_information.call_count == 1
    assert cut.spellbook.update_low_level_knowledge.call_count == 1
    assert cut.spellbook.update_low_level_knowledge.call_args_list[0].args == (fake_low_level_information, )

def test_runtime_core_run_step_does_not_query_data_source_if_override_is_given(mocker):
    # Arrange
    fake_override = MagicMock()

    cut = KastRuntime.__new__(KastRuntime)
    cut.data_source = MagicMock()
    cut.spellbook = MagicMock()
    
    mocker.patch.object(cut.data_source,'get_new_information')
    mocker.patch.object(cut.spellbook, 'update_low_level_knowledge',side_effect=Exception('short_circuit_white_mage'))

    # Act
    with pytest.raises(Exception) as einfo:
        cut.run_step(override=fake_override)

    # Assert
    assert einfo.exconly() == 'Exception: short_circuit_white_mage'
    assert cut.data_source.get_new_information.call_count == 0
    assert cut.spellbook.update_low_level_knowledge.call_count == 1
    assert cut.spellbook.update_low_level_knowledge.call_args_list[0].args == (fake_override, )

def test_runtime_core_run_step_calls_correct_sequence_of_spellbook_methods_after_updating_low_level_information(mocker):
    # Arrange
    fake_override = MagicMock()

    cut = KastRuntime.__new__(KastRuntime)
    cut.data_source = MagicMock()
    cut.spellbook = MagicMock()
    
    mocker.patch.object(cut.data_source,'get_new_information')
    mocker.patch.object(cut.spellbook, 'update_low_level_knowledge')
    mocker.patch.object(cut.spellbook, 'kast')

    # Act
    cut.run_step(override=fake_override)

    # Assert
    assert cut.data_source.get_new_information.call_count == 0
    assert cut.spellbook.update_low_level_knowledge.call_count == 1
    assert cut.spellbook.update_low_level_knowledge.call_args_list[0].args == (fake_override, )
    assert cut.spellbook.kast.call_count == 1


def test_runtime_core_runstep_prints_step_number_on_each_loop_and_calls_print_spellbook_knowledge(mocker, capsys):
    # Arrange
    step_num = pytest.gen.randint(1,10)
    fake_data_source = MagicMock()

    cut = KastRuntime.__new__(KastRuntime)
    cut.spellbook = MagicMock()
    cut.data_source = fake_data_source
    cut.data_source.index = step_num

    mocker.patch('kast.src.kast_runtime.print_spellbook_knowledge')

    # Act
    cut.run_step(io='both')
    out, _ = capsys.readouterr()

    # Assert
    assert kast.src.kast_runtime.print_spellbook_knowledge.call_count == 1
    assert f"STEP {step_num}" in out

def test_runtime_core_execute_returned_generator_returns_iterable_of_expected_form(mocker):
    # Arrange
    num_steps = pytest.gen.randint(1,10)
    fake_spellbooks = []
    fake_has_more_returns = []

    for i in range(num_steps):
        fake_spellbooks.append(MagicMock())
        if i == num_steps-1:
            fake_has_more_returns.append(False)
        else:
            fake_has_more_returns.append(True)

    cut = KastRuntime.__new__(KastRuntime)
    cut.spellbook = fake_spellbooks
    cut.data_source = MagicMock()
    
    mocker.patch.object(cut.data_source, 'has_more', side_effect=fake_has_more_returns)
    mocker.patch.object(cut, 'run_step', side_effect=fake_spellbooks)

    # Act
    yielded_spellbooks = cut.execute()


    # Assert
    for i, spellbook in enumerate(yielded_spellbooks):
        assert spellbook == fake_spellbooks[i]

def test_runtime_core_execute_prints_end_of_run_message_when_data_source_has_more_is_false(mocker,capsys):
    # Arrange
    cut = KastRuntime.__new__(KastRuntime)
    cut.data_source = MagicMock()
    cut.data_source.has_more = MagicMock(return_value=False)

    # Act
    yielded_spellbook = cut.execute()

    # Assert
    ['pass' for spellbook in yielded_spellbook] # Required to loop through runtime with generator methodology in runtime.execute
    out, _ = capsys.readouterr()
    assert cut.data_source.has_more.call_count == 1
    assert 'COMPLETE' in out

def test_runtime_core_execute_calls_run_step_while_data_source_has_more_is_true(mocker):
    # Arrange
    num_steps = pytest.gen.randint(1,10)
    has_more_returns = []

    fake_data_source = MagicMock()
    
    for i in range(num_steps):
        if i == num_steps - 1:
            has_more_returns.append(False)
        else:
            has_more_returns.append(True)
  
    cut = KastRuntime.__new__(KastRuntime)
    cut.data_source = fake_data_source

    mocker.patch.object(fake_data_source, 'has_more', side_effect=has_more_returns)
    mocker.patch.object(cut,'run_step')

    # Act
    yielded_spellbook = cut.execute()

    # Assert
    for spellbook in yielded_spellbook:
        pass # Required to loop through the list using generator methodology
    assert cut.data_source.has_more.call_count == num_steps
    assert cut.run_step.call_count == num_steps - 1


