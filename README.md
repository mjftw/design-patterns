# Example Design Patterns with Python

Example design patterns implemented in python, some written while reading
[Head First Design Patterns](https://www.oreilly.com/library/view/head-first-design/0596007124/)
and others added later.

## The patterns

Currently implemented:

- Interface
- Command
- Decorator
- Factory
- Iterator
- Proxy

## Running the tests

It is recommended that you first install the package requirements into a
virtualenv file

```shell
# Create and activate the venv
python3 -m virtualenv venv
. venv/bin/activate

# Install required packages into venv
python3 -m pip install -r requirements.txt
```

The project uses pytest to run the tests, you can therefore run them with:

```shell
python3 -m pytest
```

