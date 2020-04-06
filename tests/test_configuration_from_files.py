from pathlib import Path

from figga import Configuration


def test_from_file():
    config_file = Path(__file__).parent / "config_example_1.ini"
    config = Configuration.from_file(config_file)
    assert config.ServerAliveInterval == "45"
    assert config.ForwardX11 == "yes"
    assert config.i_dont_exist is None


def test_from_files():
    config_root = Path(__file__).parent
    config = Configuration.from_files(
        config_root / "config_example_1.ini", config_root / "config_example_2.ini"
    )
    assert config.ServerAliveInterval == "45"
    assert config.ForwardX11 == "yes"
    assert config.i_dont_exist is None
