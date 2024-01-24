import pytest
import mock
from mock import MagicMock

from kast.utils.data_sources.MANUAL_data_source import MANUALDataSource

def test_manual_data_source__init__sets_runtime_to_arg_runtime(mocker):
    # Arrange
    arg_runtime = MagicMock()
    arg_runtime.config = MagicMock()

    cut = MANUALDataSource.__new__(MANUALDataSource)

    # Action
    cut.__init__(runtime=arg_runtime)

    # Assert
    assert cut.runtime == arg_runtime

def test_manual_data_source__init__sets_index_to_zero(mocker):
    # Arrange
    arg_runtime = MagicMock()
    arg_runtime.config = MagicMock()

    cut = MANUALDataSource.__new__(MANUALDataSource)

    # Action
    cut.__init__(runtime=arg_runtime)

    # Assert
    assert cut.index == 0
        
def test_manual_data_source__init__indexes_headers_from_config_low_level_headers_by_splitting(mocker):
    # Arrange
    arg_runtime = MagicMock()
    fake_headers = MagicMock()
    arg_runtime.config = {'DEFAULT': {'LowLevelHeaders': fake_headers}}

    cut = MANUALDataSource.__new__(MANUALDataSource)

    # Action
    cut.__init__(runtime=arg_runtime)

    # Assert
    assert cut.headers == fake_headers.split(",")
        
def test_manual_data_source_get_new_information_returns_zipped_new_frame_and_increments_index(mocker):
    # Arrange
    fake_index = pytest.gen.randint(1,10)
    fake_headers = MagicMock()
    arg_frame = MagicMock()

    cut = MANUALDataSource.__new__(MANUALDataSource)
    cut.headers = fake_headers
    cut.index = fake_index

    # Action
    ret = cut.get_new_information(new_frame=arg_frame)

    # Assert
    assert ret == dict(zip(fake_headers, arg_frame))
    assert cut.index == fake_index + 1

def test_manual_data_source_has_more_returns_true(mocker):
    # Arrange
    cut = MANUALDataSource.__new__(MANUALDataSource)


    # Action
    ret = cut.has_more()

    # Assert
    assert ret == True