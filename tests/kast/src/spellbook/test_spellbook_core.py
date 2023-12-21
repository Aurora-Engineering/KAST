import pytest
from mock import MagicMock
import numpy as np

from kast.src.spellbook.core import Spellbook, Kaster
from kast.src.knowledge.core import *


def test_kaster__init__sets_self_input_vars_to_given_input_vars():
    # Arrange
    cut = Kaster.__new__(Kaster)
    arg_input_vars = MagicMock()

    # Act
    cut.__init__(arg_input_vars, None, None)

    # Assert
    assert cut.input_vars == arg_input_vars

def test_kaster__init__sets_self_output_vars_to_given_output_vars():
    # Arrange
    cut = Kaster.__new__(Kaster)
    arg_output_vars = MagicMock()

    # Act
    cut.__init__(None, arg_output_vars, None)

    # Assert
    assert cut.output_vars == arg_output_vars

def test_kaster__init__sets_self_method_to_given_method():
    # Arrange
    cut = Kaster.__new__(Kaster)
    arg_method = MagicMock()

    # Act
    cut.__init__(None, None, arg_method)

    # Assert
    assert cut.method == arg_method

def test_spellbook__init__creates_empty_data_structures_for_knowledge_and_kasters():
    # Arrange
    cut = Spellbook.__new__(Spellbook)
    fake_low_level_headers = MagicMock()
    fake_data_translation_methods = MagicMock()
    
    # Act
    cut.__init__(fake_low_level_headers,fake_data_translation_methods)

    # Assert
    assert type(cut.low_level_knowledge) == dict
    assert type(cut.high_level_knowledge) == dict
    assert type(cut.kasters) == list

def test_spellbook__init__initializes_low_level_knowledge_then_kasters_and_finally_high_level_knowledge_only_if_all_variables_required_for_kasting_exist_in_low_level_knowledge(mocker):
    
    # Arrange
    mock_manager = mocker.MagicMock()

    cut = Spellbook.__new__(Spellbook)
    fake_low_level_headers = MagicMock()
    fake_data_translation_methods = MagicMock()

    # Done to ensure these runs happen in order - data MUST be run LLK->Kasters->HLK
    mock_manager.attach_mock(mocker.patch.object(cut,'init_low_level_knowledge'),'init_low_level_knowledge')
    mock_manager.attach_mock(mocker.patch.object(cut,'init_kasters'),'init_kasters')
    mock_manager.attach_mock(mocker.patch.object(cut,'init_high_level_knowledge'),'init_high_level_knowledge')
    
    # Act
    cut.__init__(fake_low_level_headers,fake_data_translation_methods)

    # Assert
    mock_manager.assert_has_calls([
        mocker.call.init_low_level_knowledge(fake_low_level_headers),
        mocker.call.init_kasters(fake_data_translation_methods),
        mocker.call.init_high_level_knowledge()
    ], any_order=False)


def test_spellbook_init_low_level_knowledge_creates_a_dictionary_of_knowledge_objects_with_correct_names_and_length(mocker):
    # Arrange
    num_name_list_entries = np.random.randint(0,10)
    arg_name_list = []

    for i in range(num_name_list_entries):
        arg_name_list.append(MagicMock())
    
    cut = Spellbook.__new__(Spellbook)
    cut.low_level_knowledge = {}

    # Act
    cut.init_low_level_knowledge(arg_name_list)

    # Assert
    # NOTE: these checks are based on order and should break if dictionaries become unordered
    knowledge_type = type(Knowledge.__new__(Knowledge))
    assert len(cut.low_level_knowledge) == num_name_list_entries
    for i in range(num_name_list_entries):
        assert list(cut.low_level_knowledge.keys())[i] == arg_name_list[i]
        knowledge_object = list(cut.low_level_knowledge.values())[i]
        assert knowledge_object.name == arg_name_list[i]
        assert type(knowledge_object) == knowledge_type

def test_spellbook_init_kasters_creates_a_dictionary_of_kasters_with_correct_inputs_indexed_from_tuples(mocker):
    # Arrange
    num_input_tuples = np.random.randint(0,10)
    cut = Spellbook.__new__(Spellbook)

    cut.kasters = []
    arg_tuple_list = []
    fake_low_level_knowledge = {}

    for i in range(num_input_tuples):
        header = MagicMock()

        arg_tuple_list.append((header,
                               MagicMock(),
                               MagicMock()))

        fake_low_level_knowledge.update({header:MagicMock()})

    cut.low_level_knowledge = fake_low_level_knowledge
    
    # Act
    cut.init_kasters(arg_tuple_list)

    # Assert
    # NOTE: these checks are based on order and should break if dictionaries become unordered
    assert len(cut.kasters) == num_input_tuples
    for i in range(num_input_tuples):
        kaster_entry = cut.kasters[i]
        arg_tuple_entry = arg_tuple_list[i]
        assert type(kaster_entry) == Kaster
        assert kaster_entry.input_vars == arg_tuple_entry[0]
        assert kaster_entry.output_vars == arg_tuple_entry[1]
        assert kaster_entry.method == arg_tuple_entry[2]

def test_spellbook_init_kasters_throws_an_error_if_kaster_input_variable_is_not_found_in_low_level_knowledge(mocker):
    # Arrange
    cut = Spellbook.__new__(Spellbook)
    cut.low_level_knowledge = {}
    num_kasters = np.random.randint(1,10)

    arg_data_translation_methods = []
    fake_low_level_knowledge = {}
    fake_headers = []
    cut.kasters = []

    for i in range(num_kasters):
        header = MagicMock()

        fake_kaster_spec = (header,
                            None,
                            None
        )

        fake_headers.append(header)
        fake_low_level_knowledge.update({header: MagicMock()})
        arg_data_translation_methods.append(fake_kaster_spec)

    cut.low_level_knowledge = fake_low_level_knowledge

    excluded_kaster_spec = MagicMock()
    excluded_kaster_spec = ('this_is_not_in_the_low_level_knowledge',
                            None,
                            None
    )
    arg_data_translation_methods.append(excluded_kaster_spec)


    # Act
    with pytest.raises(KeyError) as e_info:
        cut.init_kasters(arg_data_translation_methods)

    # Assert
    assert f'Kaster input variable {excluded_kaster_spec[0]} was not found in the available low level knowledge.' in e_info.exconly()


def test_spellbook_init_high_level_knowledge_creates_a_list_of_high_level_knowledge_objects_with_one_for_every_kaster_using_kaster_output_variables_as_labels(mocker):

    # Arrange 
    num_kasters = np.random.randint(1,10)
    kaster_list = []
    fake_output_vars = []

    for i in range(num_kasters):
        fake_output_vars.append(MagicMock())
        kaster_list.append(Kaster(MagicMock(),fake_output_vars[i],MagicMock()))
    
    cut = Spellbook.__new__(Spellbook)
    cut.kasters = kaster_list
    cut.high_level_knowledge = {}

    # Act
    cut.init_high_level_knowledge()

    # Assert
    assert len(cut.high_level_knowledge) == num_kasters
    high_level_knowledge_keys = list(cut.high_level_knowledge.keys())
    high_level_knowledge = list(cut.high_level_knowledge.values())
    for i in range(num_kasters):
        assert high_level_knowledge_keys[i] == fake_output_vars[i]
        assert high_level_knowledge[i].name == fake_output_vars[i]

def test_spellbook_update_low_level_knowledge_updates_low_level_knowledge_dictionary_with_correct_values_from_input_data():
    
    # Arrange
    num_entries = np.random.randint(1,10)

    arg_new_frame = {}
    fake_keys = []
    fake_new_values = []

    cut = Spellbook.__new__(Spellbook)
    cut.low_level_knowledge = {}
    
    for i in range(num_entries):
        fake_key = MagicMock()
        fake_new_value = MagicMock()
        
        fake_keys.append(fake_key)
        fake_new_values.append(fake_new_value)

        cut.low_level_knowledge[fake_key] = Knowledge('low','name') # Initialize previous timestep of Knowledge objects to be updated
        arg_new_frame[fake_key] = fake_new_value
    
    # Act
    cut.update_low_level_knowledge(arg_new_frame)

    # Assert
    for i in range(num_entries):
        key = fake_keys[i]
        value = fake_new_values[i]
        assert cut.low_level_knowledge[key].value == value

def test_spellbook_update_low_level_knowledge_creates_new_knowledge_object_if_unseen_knowledge_present_in_frame():
    # Arrange
    num_entries = np.random.randint(1,10)

    arg_new_frame = {}
    fake_keys = []
    fake_new_values = []

    cut = Spellbook.__new__(Spellbook)
    cut.low_level_knowledge = {}
    
    for i in range(num_entries):
        fake_key = MagicMock()
        fake_new_value = MagicMock()
        
        fake_keys.append(fake_key)
        fake_new_values.append(fake_new_value)

        cut.low_level_knowledge[fake_key] = Knowledge('low','name') # Initialize previous timestep of Knowledge objects to be updated
        arg_new_frame[fake_key] = fake_new_value                    # Create new information for each key to be replaced with on new timestep
    
    extra_key = MagicMock() # Create a new key, not present in the low level knowledge, to create a new Knowledge representation for    
    extra_value = MagicMock()     
    arg_new_frame[extra_key] = extra_value # Give this key a value in the new frame
    
    # Act
    cut.update_low_level_knowledge(arg_new_frame)

    # Assert
    assert type(cut.low_level_knowledge[extra_key]) == Knowledge
    assert cut.low_level_knowledge[extra_key].value == extra_value


def test_kast_kaster_specified_high_level_knowledge_is_updated_with_output_of_kaster_method_called_using_kaster_specified_input_vars(mocker):
    # Arrange
    num_kasters = np.random.randint(1,10)
    fake_kasters = []
    fake_input_knowledges = []
    fake_input_values = []
    fake_output_vars = []
    fake_methods = []

    forced_returns = []

    fake_low_level_knowledge = {}
    fake_high_level_knowledge = {}

    for i in range(num_kasters):

        fake_input_name = MagicMock()

        fake_input_value = MagicMock()
        fake_input_values.append(fake_input_value)

        fake_input_knowledge = MagicMock()
        fake_input_knowledge.value = fake_input_value
        fake_input_knowledges.append(fake_input_knowledge)

        fake_output_name = MagicMock()
        fake_output_vars.append(fake_output_name)

        fake_method = MagicMock()
        fake_methods.append(fake_method)

        forced_return_output_value = MagicMock()
        forced_returns.append(forced_return_output_value)

        fake_knowledge_object = MagicMock()
        fake_low_level_knowledge[fake_input_name] = fake_input_knowledge
        fake_high_level_knowledge[fake_output_name] = fake_knowledge_object

        fake_kaster = MagicMock()
        fake_kaster.input_vars = fake_input_name
        fake_kaster.output_vars = fake_output_name

        mocker.patch.object(fake_kaster,'method',return_value=forced_return_output_value)
        mocker.patch.object(fake_knowledge_object,'update')

        fake_kasters.append(fake_kaster)
        
    cut = Spellbook.__new__(Spellbook)

    cut.low_level_knowledge = fake_low_level_knowledge
    cut.high_level_knowledge = fake_high_level_knowledge
    cut.kasters = fake_kasters

    # Act

    cut.kast()

    # Assert

    for i in range(num_kasters):
        assert fake_kasters[i].method.call_count == 1
        assert fake_kasters[i].method.call_args_list[0].args == (fake_input_values[i],)

        assert cut.high_level_knowledge[fake_output_vars[i]].update.call_count == 1
        assert cut.high_level_knowledge[fake_output_vars[i]].update.call_args_list[0].args == (forced_returns[i],)

def test_kast_does_not_update_high_level_knowledge_according_to_kaster_method_if_kaster_input_variable_is_not_present_in_low_level_knowledge(mocker):
    # Arrange
    num_kasters = np.random.randint(1,10)
    fake_kasters = []
    fake_input_knowledges = []
    fake_input_values = []
    fake_output_vars = []
    fake_methods = []

    forced_returns = []

    fake_low_level_knowledge = {}
    fake_high_level_knowledge = {}

    for i in range(num_kasters):

        fake_input_name = MagicMock()

        fake_input_value = MagicMock()
        fake_input_values.append(fake_input_value)

        fake_input_knowledge = MagicMock()
        fake_input_knowledge.value = fake_input_value
        fake_input_knowledges.append(fake_input_knowledge)

        fake_output_name = MagicMock()
        fake_output_vars.append(fake_output_name)

        fake_method = MagicMock()
        fake_methods.append(fake_method)

        forced_return_output_value = MagicMock()
        forced_returns.append(forced_return_output_value)

        fake_knowledge_object = MagicMock()
        fake_low_level_knowledge[fake_input_name] = fake_input_knowledge
        fake_high_level_knowledge[fake_output_name] = fake_knowledge_object

        fake_kaster = MagicMock()
        fake_kaster.input_vars = fake_input_name
        fake_kaster.output_vars = fake_output_name

        mocker.patch.object(fake_kaster,'method',return_value=forced_return_output_value)
        mocker.patch.object(fake_knowledge_object,'update')

        fake_kasters.append(fake_kaster)

    excluded_kaster = Kaster.__new__(Kaster)

    excluded_kaster.input_vars = MagicMock()
    excluded_kaster.output_vars = MagicMock()
    excluded_kaster.method = MagicMock()

    mocker.patch.object(excluded_kaster,'method',return_value=MagicMock())

    fake_kasters.append(excluded_kaster)
        
    cut = Spellbook.__new__(Spellbook)

    cut.low_level_knowledge = fake_low_level_knowledge
    cut.high_level_knowledge = fake_high_level_knowledge
    cut.kasters = fake_kasters 

    # Act

    cut.kast()

    # Assert
    for i in range(num_kasters):
        assert fake_kasters[i].method.call_count == 1
        
    assert excluded_kaster.method.call_count == 0

def test_kast_does_nothing_if_no_kasters_are_present(mocker):
    # Arrange

    fake_low_level_knowledge = MagicMock()
    kasters_list = []

    mocker.patch.object(fake_low_level_knowledge,'keys')

    cut = Spellbook.__new__(Spellbook)
    
    cut.low_level_knowledge = fake_low_level_knowledge
    cut.kasters = kasters_list

    # Act

    cut.kast()

    # Assert

    assert fake_low_level_knowledge.keys.call_count == 0



