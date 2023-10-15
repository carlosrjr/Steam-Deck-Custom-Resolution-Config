import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def script_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core'))

@pytest.fixture
def mock_input(monkeypatch):
    def _mock_input(value):
        return lambda _: value
    return _mock_input

@pytest.fixture
def current_dir():
    return os.path.dirname(os.path.realpath(__file__))