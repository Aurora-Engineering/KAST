import pytest
import mock
from mock import MagicMock

import os
import configparser
import numpy as np
import pandas as pd
import importlib.util

import kast
from kast.src.runtime.core import *
from kast.src.spellbook.core import Spellbook

def test_runtime_core__init__sets_internal_filepath_to_given_arg_filepath(mocker):
    # Arrange
    cut = KastRuntime.__new__(KastRuntime)
    arg_filepath = MagicMock()

    cut.data_source = MagicMock()
    cut.kaster_definitions = MagicMock()

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

    cut.data_source = fake_data_source
    cut.kaster_definitions = fake_kaster_definitions

    mocker.patch.object(cut,'parse_config')
    mocker.patch.object(cut,'import_kaster_methods')
    mocker.patch.object(cut,'initialize_data_source')
    mocker.patch('kast.src.runtime.core.Spellbook.__init__',return_value=None)

    # Action
    cut.__init__(arg_filepath)

    # Assert
    assert type(cut.spellbook) == Spellbook
    assert cut.spellbook.__init__.call_count == 1
    assert cut.spellbook.__init__.call_args_list[0].args == (fake_data_source.headers,fake_kaster_definitions)

def test_runtime_core_parse_config_generates_config_reader_and_reads_given_file(mocker):
    # Arrange 
    fake_config_filepath = MagicMock()
    fake_config = MagicMock()
    fake_config_dict = {'DEFAULT':{
                        'KasterMethodsPath': MagicMock(),
                        'KasterDefinitionsPath': MagicMock(),
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
                        'KasterDefinitionsPath': MagicMock(),
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
    assert cut.kaster_definitions_path == fake_config_dict['DEFAULT']['KasterDefinitionsPath']
    assert cut.data_file_path == fake_config_dict['DEFAULT']['DataFile']
    assert cut.data_type == fake_config_dict['DEFAULT']['DataType']

def test_runtime_core_import_kaster_methods_generates_kaster_strings_by_calling_split_on_zipped_pd_read_csv_output(mocker):
    # Arrange
    num_fake_kasters = pytest.gen.randint(1,10)
    fake_input_list = []
    fake_output_list = []
    fake_method_list = []

    fake_kaster_definitions_path = MagicMock()
    fake_kaster_df = MagicMock()

    for i in range(num_fake_kasters):
        fake_input_list.append(MagicMock())
        fake_output_list.append(MagicMock())
        fake_method_list.append(str(MagicMock()))
    
    fake_pandas_return = {'input': fake_input_list, 'output': fake_output_list, 'method': fake_method_list}
    fake_kaster_df.__getitem__.side_effect = fake_pandas_return.__getitem__

    cut = KastRuntime.__new__(KastRuntime)
    cut.kaster_definitions_path = fake_kaster_definitions_path
    cut.kaster_methods_path = MagicMock()

    mocker.patch('pandas.read_csv', return_value=fake_pandas_return)
    mocker.patch('importlib.util.spec_from_file_location',side_effect=Exception('short_circuit_dragoon'))

    # Act
    with pytest.raises(Exception) as einfo:
        cut.import_kaster_methods()

    # Assert
    assert einfo.exconly() == 'Exception: short_circuit_dragoon'

    assert pd.read_csv.call_count == 1
    assert pd.read_csv.call_args_list[0].args == (fake_kaster_definitions_path, )

    for i in range(num_fake_kasters):
        assert fake_input_list[i].split.call_count == 1
        assert fake_output_list[i].split.call_count == 1

def test_runtime_core_import_kaster_sets_self_kaster_definitions_to_list_of_tuples_of_split_strings_and_callable_versions_of_pandas_output(mocker):
    # Arrange
    num_fake_kasters = pytest.gen.randint(1,10)
    fake_input_list = []
    fake_output_list = []
    fake_method_list = []
    fake_callables_list = []

    fake_kaster_methods_path = MagicMock()
    fake_spec = MagicMock()
    fake_module = MagicMock()

    for i in range(num_fake_kasters):
        fake_input_list.append(MagicMock())
        fake_output_list.append(MagicMock())
        fake_method_list.append(str(MagicMock()))
        fake_callables_list.append(MagicMock())
    
    fake_pandas_return = {'input': fake_input_list, 'output': fake_output_list, 'method': fake_method_list}

    cut = KastRuntime.__new__(KastRuntime)
    cut.kaster_definitions_path = MagicMock()
    cut.kaster_methods_path = fake_kaster_methods_path

    mocker.patch('pandas.read_csv', return_value=fake_pandas_return)
    mocker.patch('importlib.util.spec_from_file_location',return_value=fake_spec)
    mocker.patch('importlib.util.module_from_spec',return_value=fake_module)
    
    mocker.patch.object(fake_spec,'loader.exec_module')
    mocker.patch('kast.src.runtime.core.get_attribute_by_name',side_effect=fake_callables_list)

    # Act
    cut.import_kaster_methods()

    # Assert
    assert len(cut.kaster_definitions) == num_fake_kasters
    assert kast.src.runtime.core.get_attribute_by_name.call_count == num_fake_kasters
    for i in range(num_fake_kasters):
        assert kast.src.runtime.core.get_attribute_by_name.call_args_list[i].args == (fake_module, fake_method_list[i])
        assert cut.kaster_definitions[i] == (fake_input_list[i].split(),fake_output_list[i].split(),fake_callables_list[i])
    
def test_runtime_core_initialize_data_source_imports_datatype_specified_data_source_using_importmodule_then_sets_internal_data_source_to_instance_of_imported_class(mocker):
    # Arrange
    fake_data_type = MagicMock()
    fake_module = MagicMock()
    fake_class_reference = MagicMock()

    cut = KastRuntime.__new__(KastRuntime)
    cut.data_type = fake_data_type

    mocker.patch('kast.src.runtime.core.import_module',return_value=fake_module)
    mocker.patch('kast.src.runtime.core.get_attribute_by_name',return_value=fake_class_reference)
    
    # Act
    cut.initialize_data_source()

    # Assert
    assert kast.src.runtime.core.import_module.call_count == 1
    assert kast.src.runtime.core.import_module.call_args_list[0].kwargs == {'module_name': 'data_source', 'file_to_import': f'kast/utils/data_sources/{cut.data_type}_data_source.py'}
    assert kast.src.runtime.core.get_attribute_by_name.call_count == 1
    assert kast.src.runtime.core.get_attribute_by_name.call_args_list[0].args == (fake_module,f'{cut.data_type.upper()}DataSource')
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

def test_runtime_core_execute_prints_end_of_run_message_when_data_source_has_more_is_false(mocker,capsys):
    # Arrange
    cut = KastRuntime.__new__(KastRuntime)
    cut.data_source = MagicMock()
    cut.data_source.has_more = MagicMock(return_value=False)

    # Act
    cut.execute()
    out, _ = capsys.readouterr()

    # Assert
    assert 'RUN COMPLETE' in out

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
    cut.execute()

    # Assert
    assert cut.data_source.has_more.call_count == num_steps
    assert cut.run_step.call_count == num_steps - 1

def test_runtime_core_execute_prints_step_number_on_each_loop(mocker, capsys):
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
    cut.execute()
    out, _ = capsys.readouterr()

    # Assert
    assert cut.data_source.has_more.call_count == num_steps
    assert cut.run_step.call_count == num_steps - 1
    assert out.count('STEP') == num_steps - 1

def test_runtime_core_execute_prints_high_level_knowledge_only_when_io_arg_passed_as_high(mocker, capsys):
    # Arrange
    has_more_returns = [True, False]

    fake_data_source = MagicMock()
    fake_high_level_knowledge_value = MagicMock()

    cut = KastRuntime.__new__(KastRuntime)
    cut.data_source = fake_data_source
    cut.spellbook = MagicMock()
    cut.spellbook.high_level_knowledge = {MagicMock(): fake_high_level_knowledge_value}

    mocker.patch.object(fake_data_source, 'has_more', side_effect=has_more_returns)
    mocker.patch.object(cut,'run_step')

    # Act
    cut.execute(io='high')
    out, _ = capsys.readouterr()
    print(out)

    # Assert
    assert cut.run_step.call_count == 1
    assert str(fake_high_level_knowledge_value) in out


def test_runtime_core_execute_prints_low_level_knowledge_only_when_io_arg_passed_as_low(mocker, capsys):
    # Arrange
    has_more_returns = [True, False]

    fake_data_source = MagicMock()
    fake_low_level_knowledge_value = MagicMock()

    cut = KastRuntime.__new__(KastRuntime)
    cut.data_source = fake_data_source
    cut.spellbook = MagicMock()
    cut.spellbook.low_level_knowledge = {MagicMock(): fake_low_level_knowledge_value}

    mocker.patch.object(fake_data_source, 'has_more', side_effect=has_more_returns)
    mocker.patch.object(cut,'run_step')

    # Act
    cut.execute(io='low')
    out, _ = capsys.readouterr()
    print(out)

    # Assert
    assert cut.run_step.call_count == 1
    assert str(fake_low_level_knowledge_value) in out

def test_runtime_core_execute_prints_both_high_and_low_level_knowledge_only_when_io_arg_passed_as_both(mocker, capsys):
    # Arrange
    has_more_returns = [True, False]

    fake_data_source = MagicMock()
    fake_low_level_knowledge_value = MagicMock()
    fake_high_level_knowledge_value = MagicMock()

    cut = KastRuntime.__new__(KastRuntime)
    cut.data_source = fake_data_source
    cut.spellbook = MagicMock()
    cut.spellbook.low_level_knowledge = {MagicMock(): fake_low_level_knowledge_value}
    cut.spellbook.high_level_knowledge = {MagicMock(): fake_high_level_knowledge_value}

    mocker.patch.object(fake_data_source, 'has_more', side_effect=has_more_returns)
    mocker.patch.object(cut,'run_step')

    # Act
    cut.execute(io='both')
    out, _ = capsys.readouterr()
    print(out)

    # Assert
    assert cut.run_step.call_count == 1
    assert str(fake_high_level_knowledge_value) in out
    assert str(fake_low_level_knowledge_value) in out
