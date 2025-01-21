# GSC-19360-1, "Knowledge Acquisition and Synthesis Tool"
#
# Copyright © 2024 United States Government as represented by the 
# Administrator of the National Aeronautics and Space Administration.   
# All Rights Reserved.
#
# Licensed under the NASA Open Source Agreement version 1.3
# See "NOSA GSC-19360-1 KAST.pdf"

import kast
import pytest
import random
from time import time
from unittest.mock import MagicMock
import sys

def pytest_addoption(parser):
  parser.addoption("--conftest-seed", action="store", type=int, default=None)

def pytest_configure(config):
  seed = config.getoption("--conftest-seed")
  if config.getoption("--conftest-seed") == None:
    seed = int(time())
  pytest.gen = random.Random(seed)
  print(f"Using --conftest-seed={seed}")