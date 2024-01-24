import pytest
from mock import MagicMock
import importlib.util
import os

from kast.utils.functions import import_module, get_attribute_by_name

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