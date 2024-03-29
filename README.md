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

Once your're good with the updates, on your feature-branch:

1. Making changes
2. Add new function in file `__init__.py`
   1. Add in import
   2. Add in `__all__`
3. Increase version in setup.cfg
4. Format, test and lint
5. Create a new version with this command:
```bash
pip uninstall -y flask_utils && pip install -v . --no-cache-dir
```
6. Add, commit, and Push your changes
7. Then run this command to tag your commit, where the tag corresponds to the new version
```bash
$ git tag -a vX.X.X -m "Version message"
$ git push origin vX.X.X
```
8. Finally, create a release on github (Code > Release> Draft a new Release) with the new tag, publish it, and merge the pull request
