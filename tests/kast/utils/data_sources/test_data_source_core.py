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

from kast.utils.data_sources.core import DataSource

def test_data_source_core__init__raises_not_implemented_error(mocker):
    # Arrange
    cut = DataSource.__new__(DataSource)

    # Action
    with pytest.raises(NotImplementedError):
        cut.__init__()

    # Assert
    # Pytest raises does this!
        
def test_data_source_core_get_new_information_raises_not_implemented_error(mocker):
    # Arrange
    cut = DataSource.__new__(DataSource)

    # Action
    with pytest.raises(NotImplementedError):
        cut.get_new_information()

    # Assert
    # Pytest raises does this!
        
def test_data_source_core_has_more_raises_not_implemented_error(mocker):
    # Arrange
    cut = DataSource.__new__(DataSource)

    # Action
    with pytest.raises(NotImplementedError):
        cut.has_more()

    # Assert
    # Pytest raises does this!
        