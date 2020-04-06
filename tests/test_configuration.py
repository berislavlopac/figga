import pytest

from figga import Configuration


@pytest.fixture
def config_dict():
    return {
        "ServerAliveInterval": 45,
        "Compression": "yes",
        "CompressionLevel": "9",
        "ForwardX11": "yes",
    }


def test_getattr(config_dict):
    config = Configuration(config_dict)
    assert config.ServerAliveInterval == 45
    assert config.ForwardX11 == "yes"
    assert config.i_dont_exist is None


def test_getattr_custom_default_value(config_dict):
    config = Configuration(config_dict, default="foo bar")
    assert config.ServerAliveInterval == 45
    assert config.ForwardX11 == "yes"
    assert config.i_dont_exist == "foo bar"


def test_getattr_callable_default_value(config_dict):
    config = Configuration(config_dict, default=lambda x: f"I am custom: {x}")
    assert config.ServerAliveInterval == 45
    assert config.ForwardX11 == "yes"
    assert config.i_do_not_exist == "I am custom: i_do_not_exist"


def test_getattr_exception_default_value(config_dict):
    config = Configuration(config_dict, default=ValueError)
    assert config.ServerAliveInterval == 45
    assert config.ForwardX11 == "yes"
    with pytest.raises(ValueError):
        config.i_do_not_exist


def test_items(config_dict):
    config = Configuration(config_dict)
    expected = [
        ("compressionlevel", "9"),
        ("compression", "yes"),
        ("serveraliveinterval", 45),
        ("forwardx11", "yes"),
    ]
    assert sorted(config.items()) == sorted(expected)


def test_get(config_dict):
    config = Configuration(config_dict)
    assert config.get("CompressionLevel") == "9"


def test_get_default(config_dict):
    config = Configuration(config_dict, default="foo")
    assert config.get("nonexistant") == "foo"
    assert config.get("nonexistant", default=None) is None
