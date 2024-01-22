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