import argparse
import subprocess
import sys
import os
import pytest
from unittest.mock import patch, call
from core.custom_refresh_rate_steam_deck import confirm_execution, read_args, execute_custom_resolution_configuration, execute_configuration_manually

def test_confirm_execution_yes_input_with_y():
    with patch('builtins.input', return_value='y'):
        assert confirm_execution() is True

def test_confirm_execution_yes_input():
    with patch('builtins.input', return_value='yes'):
        assert confirm_execution() is True

def test_confirm_execution_no_input():
    with patch('builtins.input', return_value='n'):
        assert confirm_execution() is False

@patch('core.custom_refresh_rate_steam_deck.argparse.ArgumentParser.parse_args')
def test_read_args_default_values(mock_parse_args):
    mock_parse_args.return_value = argparse.Namespace(width=2560, height=1080, output='DisplayPort-0', refresh_rate=120, manual=False)
    
    args = read_args()
    assert args.width == 2560
    assert args.height == 1080
    assert args.output == 'DisplayPort-0'
    assert args.refresh_rate == 120
    assert not args.manual

def test_execute_custom_resolution_configuration_with_no_setcustomres(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    with patch('subprocess.run', side_effect=FileNotFoundError):
        execute_custom_resolution_configuration(1920, 1080, 'HDMI-0', 60)

@patch('builtins.input', return_value='n')
@patch('subprocess.check_output', return_value='Modeline "2560x1080_75.00"  294.00  2560 2744 3016 3472  1080 1083 1093 1130 -hsync +vsync')
def test_execute_configuration_manually_with_wrong_input(mock_check_output, mock_input):
    with patch('subprocess.run') as mock_run:
        execute_configuration_manually(2560, 1080, 75, 'HDMI-0')
        mock_run.assert_not_called()

def test_execute_custom_resolution_configuration_with_setcustomres(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    with patch('subprocess.run') as mock_run:
        execute_custom_resolution_configuration(1920, 1080, 'HDMI-0', 60)
        mock_run.assert_called()

def test_execute_custom_resolution_configuration_without_setcustomres(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    with patch('subprocess.run', side_effect=FileNotFoundError):
        execute_custom_resolution_configuration(1920, 1080, 'HDMI-0', 60)

def test_execute_custom_resolution_configuration(monkeypatch):
    with patch('builtins.input', return_value='y') as mock_input:
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = [None, None]  # Mock two subprocess.run calls
            execute_custom_resolution_configuration(1920, 1080, 'HDMI-0', 60)
            mock_run.assert_called_with(
                ["/usr/bin/setcustomres", "-w", "1920", "-h", "1080", "-o", "HDMI-0", "-r", "60"]
            )
            assert mock_run.call_count == 2
            mock_run.assert_has_calls([
                call(['setcustomres', '-v'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL),
                call(["/usr/bin/setcustomres", "-w", "1920", "-h", "1080", "-o", "HDMI-0", "-r", "60"])
            ], any_order=False)
