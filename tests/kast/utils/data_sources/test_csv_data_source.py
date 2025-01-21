# GSC-19360-1, "Knowledge Acquisition and Synthesis Tool"
#
# Copyright © 2024 United States Government as represented by the 
# Administrator of the National Aeronautics and Space Administration.   
# All Rights Reserved.
#
# Licensed under the NASA Open Source Agreement version 1.3
# See "NOSA GSC-19360-1 KAST.pdf"

import pytest
from mock import MagicMock

import numpy as np

from kast.utils.data_sources.csv_data_source import CsvDataSource

def test_csv_data_source__init__sets_runtime_to_given_runtime(mocker):
    # Arrange
    cut = CsvDataSource.__new__(CsvDataSource)
    fake_runtime = MagicMock()

    mocker.patch('csv.reader', side_effect=Exception('short-circuit red mage'))

    # Action
    with pytest.raises(Exception)as einfo:
        cut.__init__(fake_runtime)

    # Assert
    assert cut.runtime == fake_runtime
    assert einfo.exconly() == 'Exception: short-circuit red mage'

def test_csv_data_source__init__sets_data_to_numpy_array_result_of_csv_reader_then_retrieves_headers_and_finally_sets_index_to_1(mocker):
    # Arrange
    cut = CsvDataSource.__new__(CsvDataSource)
    fake_runtime = MagicMock()
    fake_open_return = MagicMock()
    fake_reader_return = [MagicMock()]

    mocker.patch('builtins.open',return_value=fake_open_return)
    mocker.patch('csv.reader', return_value=fake_reader_return)
    mocker.patch('numpy.array')

    # Action
    cut.__init__(fake_runtime)

    # Assert
    assert open.call_count == 1
    assert open.call_args_list[0].args == (fake_runtime.data_file_path, 'r')
    assert np.array.call_count == 1
    assert np.array.call_args_list[0].args == (list(fake_reader_return), )
    assert cut.headers == np.array(list(fake_reader_return))[0]
    assert cut.index == 0

def test_csv_data_source_get_new_information_queries_internal_data_by_index_then_zips_with_headers_and_returns_new_information_dict(mocker):
    # Arrange
    num_fake_internal_data = pytest.gen.randint(2,10)
    fake_internal_data = []
    for i in range(num_fake_internal_data):
        fake_internal_data.append(MagicMock())

    fake_index = pytest.gen.randint(0,num_fake_internal_data-1)

    fake_headers = MagicMock()

    cut = CsvDataSource.__new__(CsvDataSource)
    cut.index = fake_index
    cut.data = fake_internal_data
    cut.headers = fake_headers

    # Act
    ret = cut.get_new_information()

    # Assert
    assert ret == dict(zip(fake_headers, fake_internal_data[fake_index]))

def test_csv_data_source_get_new_information_increments_index(mocker):
    # Arrange
    num_fake_internal_data = pytest.gen.randint(2,10)
    fake_internal_data = []
    for i in range(num_fake_internal_data):
        fake_internal_data.append(MagicMock())

    fake_index = pytest.gen.randint(0,num_fake_internal_data-1)

    cut = CsvDataSource.__new__(CsvDataSource)
    cut.index = fake_index
    cut.data = fake_internal_data
    cut.headers = MagicMock()

    # Act
    ret = cut.get_new_information()

    # Assert
    assert cut.index == fake_index + 1

def test_csv_data_source_has_more_returns_true_when_index_is_less_than_length_of_internal_data(mocker):
    # Arrange
    fake_data = MagicMock()
    fake_length = pytest.gen.randint(1,10)
    index = fake_length - 1

    mocker.patch('kast.utils.data_sources.csv_data_source.len', return_value=fake_length)

    cut = CsvDataSource.__new__(CsvDataSource)
    cut.data = fake_data
    cut.index = index

    # Act
    ret = cut.has_more()

    # Assert
    ret == True

def test_csv_data_source_has_more_returns_false_when_index_is_greater_than_length_of_internal_data(mocker):
    # Arrange
    fake_data = MagicMock()
    fake_length = pytest.gen.randint(1,10)
    index = fake_length + 1

    mocker.patch('kast.utils.data_sources.csv_data_source.len', return_value=fake_length)

    cut = CsvDataSource.__new__(CsvDataSource)
    cut.data = fake_data
    cut.index = index

    # Act
    ret = cut.has_more()

    # Assert
    ret == False

def test_csv_data_source_has_more_returns_false_when_index_is_equal_to_length_of_internal_data(mocker):
    # Arrange
    fake_data = MagicMock()
    fake_length = pytest.gen.randint(1,10)
    index = fake_length

    mocker.patch('kast.utils.data_sources.csv_data_source.len', return_value=fake_length)

    cut = CsvDataSource.__new__(CsvDataSource)
    cut.data = fake_data
    cut.index = index

    # Act
    ret = cut.has_more()

    # Assert
    ret == False