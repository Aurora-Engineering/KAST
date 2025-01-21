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

from kast.utils.data_sources.live_data_source import LiveDataSource

def test_live_data_source__init__sets_runtime_to_arg_runtime(mocker):
    # Arrange
    arg_runtime = MagicMock()
    arg_runtime.config = MagicMock()

    cut = LiveDataSource.__new__(LiveDataSource)

    # Action
    cut.__init__(runtime=arg_runtime)

    # Assert
    assert cut.runtime == arg_runtime

def test_live_data_source__init__sets_index_to_zero(mocker):
    # Arrange
    arg_runtime = MagicMock()
    arg_runtime.config = MagicMock()

    cut = LiveDataSource.__new__(LiveDataSource)

    # Action
    cut.__init__(runtime=arg_runtime)

    # Assert
    assert cut.index == 0
        
def test_live_data_source__init__sets_headers_from_runtime(mocker):
    ### FIX ###
    # Arrange
    arg_runtime = MagicMock()
    fake_headers = MagicMock()

    arg_runtime.headers = fake_headers

    cut = LiveDataSource.__new__(LiveDataSource)

    # Action
    cut.__init__(runtime=arg_runtime)

    # Assert
    assert cut.headers == fake_headers
        
def test_live_data_source_get_new_information_returns_zipped_new_frame_and_increments_index(mocker):
    # Arrange
    fake_index = pytest.gen.randint(1,10)
    fake_headers = MagicMock()
    arg_frame = MagicMock()

    cut = LiveDataSource.__new__(LiveDataSource)
    cut.headers = fake_headers
    cut.index = fake_index

    # Action
    ret = cut.get_new_information(new_frame=arg_frame)

    # Assert
    assert ret == dict(zip(fake_headers, arg_frame))
    assert cut.index == fake_index + 1

def test_live_data_source_has_more_returns_true(mocker):
    # Arrange
    cut = LiveDataSource.__new__(LiveDataSource)

    # Action
    ret = cut.has_more()

    # Assert
    assert ret == True