from pathlib import Path

from src.tools.tools import run_command, load_cas_credentials
from src.tools.logger import logger
import pytest
from unittest.mock import patch

@pytest.fixture
def mock_logger_error(mocker):
    return mocker.patch.object(logger, 'error')

@pytest.fixture
def mock_logger_debug(mocker):
    return mocker.patch.object(logger, 'debug')

def test_run_command_success(mock_logger_debug):
    command = ["echo", "hello"]
    result = run_command(command)
    assert result.returncode == 0
    assert "hello" in result.stdout
    mock_logger_debug.assert_called_once_with(f"Running command: {' '.join(command)}")


def test_run_command_failure_raise(mock_logger_error):
    command = ["false"]
    with pytest.raises(RuntimeError, match="Command failed"):
        run_command(command)
    mock_logger_error.assert_called_once_with("Command failed: false\n")

def test_run_command_failure_no_raise(mock_logger_error):
    command = ["false"]
    result = run_command(command, raise_on_failure=False)
    assert result.returncode != 0
    mock_logger_error.assert_called_once_with("Command failed: false\n")

def test_run_command_without_log():
    command = ["false"]
    with patch.object(logger, 'error') as mock_error:
        run_command(command, without_log=True, raise_on_failure=False)
        mock_error.assert_not_called()

def test_run_command_with_shell(mock_logger_debug):
    command = "echo hello"
    result = run_command(command, shell=True)
    assert result.returncode == 0
    assert "hello" in result.stdout
    mock_logger_debug.assert_called_once_with(f"Running command: {command}")

def test_run_command_empty_output(mock_logger_debug):
    command = ["true"]
    result = run_command(command)
    assert result.returncode == 0
    assert result.stdout == ""
    mock_logger_debug.assert_called_once_with("Running command: true")

def test_run_command_with_stderr(mock_logger_error):
    command = ["ls", "/nonexistent_directory"]
    with pytest.raises(RuntimeError, match="Command failed"):
        run_command(command)

    logged_error = mock_logger_error.call_args[0][0]
    assert "No such file or directory" in logged_error
    assert "ls /nonexistent_directory" in logged_error

def test_run_command_no_raise_on_failure(mock_logger_error):
    command = ["false"]
    result = run_command(command, raise_on_failure=False)
    assert result.returncode != 0
    mock_logger_error.assert_called_once_with("Command failed: false\n")

def test_run_command_without_log(mock_logger_error, mock_logger_debug):
    command = ["false"]
    run_command(command, raise_on_failure=False, without_log=True)
    mock_logger_debug.assert_not_called()
    mock_logger_error.assert_not_called()

def test_run_command_long_output(mock_logger_debug):
    command = ["seq", "1", "1000"]
    result = run_command(command)
    assert result.returncode == 0
    assert len(result.stdout.splitlines()) == 1000
    mock_logger_debug.assert_called_once_with("Running command: seq 1 1000")



def test_load_cas_credentials_success(mocker):
    mock_file_content = """
    immudb_username: test_user
    immudb_password: test_pass
    immudb_database: test_db
    immudb_address: localhost
    """
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data=mock_file_content))
    credentials = load_cas_credentials()
    assert credentials == {
        "username": "test_user",
        "password": "test_pass",
        "database": "test_db",
        "immudb_address": "localhost",
    }
    mock_open.assert_called_once_with(Path("~/.cas/credentials").expanduser())

def test_load_cas_credentials_file_not_found(mock_logger_error):
    with pytest.raises(FileNotFoundError):
        load_cas_credentials("/invalid/path")
    mock_logger_error.assert_called_once_with("Credentials file not found at /invalid/path")

def test_load_cas_credentials_missing_keys(mocker):
    mock_file_content = """
    immudb_username: test_user
    """
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_file_content))
    with pytest.raises(KeyError):
        load_cas_credentials()

def test_load_cas_credentials_empty_file(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data=""))
    with pytest.raises(ValueError, match="empty or contains invalid content"):
        load_cas_credentials()

def test_load_cas_credentials_partial_data(mocker):
    mock_file_content = """
    immudb_username: test_user
    immudb_password: test_pass
    """
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_file_content))
    with pytest.raises(KeyError):
        load_cas_credentials()

def test_load_cas_credentials_custom_path(mocker):
    custom_path = "/tmp/custom_credentials.yaml"
    mock_file_content = """
    immudb_username: user
    immudb_password: pass
    immudb_database: test_db
    immudb_address: 127.0.0.1
    """
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_file_content))
    credentials = load_cas_credentials(custom_path)
    assert credentials == {
        "username": "user",
        "password": "pass",
        "database": "test_db",
        "immudb_address": "127.0.0.1",
    }

def test_load_cas_credentials_invalid_format(mocker):
    mock_file_content = "{username: unclosed string"
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_file_content))
    with pytest.raises(Exception):
        load_cas_credentials()

def test_load_cas_credentials_logging_success(mocker, mock_logger_debug):
    mock_file_content = """
    immudb_username: test_user
    immudb_password: test_pass
    immudb_database: test_db
    immudb_address: localhost
    """
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_file_content))
    load_cas_credentials()
    mock_logger_debug.assert_not_called()
