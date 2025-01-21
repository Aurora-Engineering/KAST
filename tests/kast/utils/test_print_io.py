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

from kast.utils.print_io import *

def test_print_spellbook_knowledge_prints_nothing_if_io_is_not_given(mocker, capsys):
    # Arrange
    arg_io = False
    arg_runtime = MagicMock()

    # Act
    print_spellbook_knowledge(arg_runtime)
    out, _ = capsys.readouterr()

    # Assert
    assert out == ''


def test_print_spellbook_knowledge_prints_high_level_knowledge_only_when_io_arg_passed_as_high(mocker, capsys):
    # Arrange
    fake_data_source = MagicMock()
    fake_high_level_knowledge_value = MagicMock()
    arg_runtime = MagicMock()

    arg_runtime.data_source = fake_data_source
    arg_runtime.spellbook = MagicMock()
    arg_runtime.spellbook.high_level_knowledge = {MagicMock(): fake_high_level_knowledge_value}

    # Act
    print_spellbook_knowledge(arg_runtime,io='high')
    out, _ = capsys.readouterr()

    # Assert
    assert str(fake_high_level_knowledge_value) in out


def test_print_spellbook_knowledge_prints_low_level_knowledge_only_when_io_arg_passed_as_low(mocker, capsys):
    # Arrange
    fake_data_source = MagicMock()
    fake_low_level_knowledge_value = MagicMock()
    arg_runtime = MagicMock()

    arg_runtime.data_source = fake_data_source
    arg_runtime.spellbook = MagicMock()
    arg_runtime.spellbook.low_level_knowledge = {MagicMock(): fake_low_level_knowledge_value}

    # Act
    print_spellbook_knowledge(arg_runtime,io='low')
    out, _ = capsys.readouterr()

    # Assert
    assert str(fake_low_level_knowledge_value) in out

def test_print_spellbook_knowledge_prints_both_high_and_low_level_knowledge_only_when_io_arg_passed_as_both(mocker, capsys):
    # Arrange
    fake_data_source = MagicMock()
    fake_low_level_knowledge_value = MagicMock()
    fake_high_level_knowledge_value = MagicMock()
    arg_runtime = MagicMock()

    arg_runtime.data_source = fake_data_source
    arg_runtime.spellbook = MagicMock()
    arg_runtime.spellbook.low_level_knowledge = {MagicMock(): fake_low_level_knowledge_value}
    arg_runtime.spellbook.high_level_knowledge = {MagicMock(): fake_high_level_knowledge_value}

    # Act
    print_spellbook_knowledge(arg_runtime,io='both')
    out, _ = capsys.readouterr()

    # Assert
    assert str(fake_high_level_knowledge_value) in out
    assert str(fake_low_level_knowledge_value) in out