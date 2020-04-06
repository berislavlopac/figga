import os

import pytest

from figga import Configuration


@pytest.fixture
def env_vars():
    test_vars = {
        "FIG_VAR1": "foo",
        "FIG_VAR2": "123",
        "FIG_VAR3": "bar",
    }
    original_vars = {key: os.getenv(key, None) for key in test_vars}
    os.environ.update(test_vars)
    yield test_vars
    for var, val in original_vars.items():
        if val is None:
            os.unsetenv(var)
        else:
            os.environ[var] = val


def test_from_environ(env_vars):
    config = Configuration.from_environ(prefix="FIG_")
    assert config.fig_var1 == "foo"
    assert config.fig_var2 == "123"
    assert config.fig_var3 == "bar"


def test_from_environ_remove_prefix(env_vars):
    config = Configuration.from_environ(prefix="FIG_", remove_prefix=True)
    assert config.var1 == "foo"
    assert config.var2 == "123"
    assert config.var3 == "bar"
