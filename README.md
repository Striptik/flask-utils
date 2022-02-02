## Table of Contents

1. [Testing](#testing)
2. [Lint](#lint)
3. [Format](#format)
4. [Build Package](#build-package)

## Testing

To add a unit test, simply create a `test_*.py` file anywhere in `./test/`, prefix your test classes with `Test` and your testing methods with `test_`. Unittest will run them automatically.
You can add objects in your database that will only be used in your tests, see example.
You can run your tests in their own container with the command:

```bash
$ make test
```

## Lint

To lint your code using flake8, just run in your terminal:

```bash
$ make test.lint
```

It will run the flake8 commands on your project in your server container, and display any lint error you may have in your code.

## Format

The code is formatted using [Black](https://github.com/python/black) and [Isort](https://pypi.org/project/isort/). You have the following commands to your disposal:

```bash
$ make format
```

## Build package

On your feature-branch, increase version in setup.cfg and run this command before commit

```bash
pip uninstall -y flask_utils && pip install -v .
```
