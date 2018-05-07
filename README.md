# figga

A very simple configuration manager for Python.

[![Travis CI build](https://www.travis-ci.org/berislavlopac/figga.svg?branch=master)](https://www.travis-ci.org/berislavlopac/figga)


## Usage

`figga` currently supports three ways of specifying the configuration:

* standard Python dictionary
* environment variables with a common prefix
* one or more `INI` files


### Basic Usage

The default mechanism of instantiating a `figga.Configuration` instance is passing a simple Python dictionary:

    from figga import Configuration

    config = Configuration({'foo': 'bar', 'var1': 123, 'VAR2': 'buzz'})

This mechanism can be easily used to store configuration in any file format which can easily be converted to a `dict`, such as JSON or YAML:

    import json
    from figga import Configuration

    with open('config.json') as json_config:
        config = Configuration(json.load(json_config))

The instantiated object can be used from elsewhere in your code, e.g. if the above instantiation happened in module `somewhere.py`:

    from somewhere import config

    print(config.some_value)

Note that all variable names are normalised to lowercase, and access is case insensitive: `config.foo`, `config.FOO` or `config.Foo` all point to the same value.

In addition to direct access, values can be retrieved using the `get` method:

    config.get('some_value')

Note that `get` also accepts the `default` argument, the value of which will override the default value specified at instantiation (see below).


### Default Values

All constructor methods accept the argument `default`, which defines the behaviour when a non-existing value is accessed. This argument can handle three different types of default values:

* any object or scalar value, which will be returned as-is
* a callable, which will be called passing the accessed variable name as the only argument, returning its result
* a `BaseException` subclass, which will be raised instead of returning a value

If no default value is specified, an unknown variable will have the value of `None`.


### From Environment Variables

Another option to initialize the configuration manager is by taking the values of all the environment variables which begin with a common prefix:

    import os
    from figga import Configuration

    os.environ['YOURAPP_VARIABLE'] = 'foo bar'

    config = Configuration.from_environ(prefix='YOURAPP_')

    print(config.yourapp_variable)

Optionally you can remove the prefix from the final configuration variables:

    config = Configuration.from_environ(prefix='YOURAPP_', remove_prefix=True)

    print(config.variable)


### From INI Files

Alternatively, `figga.Configuration` can be instantiated using one or more [configparser](https://docs.python.org/3/library/configparser.html)-compatible files:

    from figga import Configuration

    config = Configuration.from_files('config1.ini', '/vars/config2.ini')

If the file paths are not absolute, they are assumed to be relative to the current working directory. Paths can be either strings or `os.PathLike` instances.
