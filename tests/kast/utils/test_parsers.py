import pytest
from mock import MagicMock, patch
import pandas as pd
import builtins

from kast.utils.parsers import *

def test__init__sets_df_to_readcsv_output_of_given_filename(mocker):
    # Arrange
    fake_filename = MagicMock()
    forced_df_output = MagicMock()

    mocker.patch('pandas.read_csv',return_value=forced_df_output)

    cut = CSVParser.__new__(CSVParser)
    
    # Act
    cut.__init__(fake_filename)

    # Assert
    pd.read_csv.assert_called_with(fake_filename)
    assert cut.df == forced_df_output

def test__init__sets__iterator_to_output_of_itertuples_call(mocker):
    # Arrange
    fake_df = MagicMock()
    fake_iterator_obj = MagicMock()

    mocker.patch.object(fake_df,'itertuples',return_value=fake_iterator_obj)
    mocker.patch('pandas.read_csv',return_value=fake_df)

    cut = CSVParser.__new__(CSVParser)
    
    # Act
    cut.__init__(None)

    # Assert
    assert fake_df.itertuples.call_count == 1
    assert cut._iterator == fake_iterator_obj

def test_get_next_mapped_line_gets_next_iterator_value_and_returns_value_if_next_call_does_not_return_none(mocker):
    # Arrange
    cut = CSVParser.__new__(CSVParser)

    fake_returned_value = MagicMock()
    fake_dictionary = MagicMock()
    fake_iterator = MagicMock()

    mocked_next_call = MagicMock(return_value=fake_returned_value)
    mocker.patch.object(fake_returned_value,'_asdict',return_value=fake_dictionary)

    cut._iterator = fake_iterator

    # Act
    with patch('builtins.next', mocked_next_call):
        ret = cut.get_next_mapped_line()

    # Assert
    mocked_next_call.assert_called_once_with(fake_iterator,None)
    assert fake_returned_value._asdict.call_count == 1
    assert ret == fake_dictionary

def test_get_next_mapped_line_returns_none_if_next_call_returns_none(mocker):
    # Arrange
    cut = CSVParser.__new__(CSVParser)

    forced_return_value = None
    fake_iterator = MagicMock()

    mocked_next_call = MagicMock(return_value=forced_return_value)

    cut._iterator = fake_iterator

    # Act
    with patch('builtins.next', mocked_next_call):
        ret = cut.get_next_mapped_line()

    # Assert
    mocked_next_call.assert_called_once_with(fake_iterator,None)
    assert ret == None