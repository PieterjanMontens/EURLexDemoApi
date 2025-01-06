[![Generic badge](https://img.shields.io/badge/Type%3F-demo-orange.svg)](https://shields.io)
[![Generic badge](https://img.shields.io/badge/Status-Unofficial-red.svg)](https://eur-lex.europa.eu/)

# EURLex Demo Api

Unofficial test API for EUR-Lex

Objective:

- Provide search endpoints similar to existing webservice
- Provide easy-to-use navigation endpoints


## Installation
Clone the repository to your directory of choice:
```bash
> git clone https://github.com/PieterjanMontens/EURLexDemoApi
> cd EURLexDemoApi
```

Once in the root directory, you can run the API with docker (for testing) or using poetry (for development).

```bash
# docker
> docker build -t "api" ./  && docker run --rm -it -p 5000:5000 api

# poetry
> poetry install
```

### Poetry installation
Poetry installs a local, isolated python environment, to avoid conflicts with your system's python modules. See [here](https://python-poetry.org/docs/).

A recent [python](https://www.python.org/downloads/) version (>=3.11) will also be needed.

## Usage
```bash
# Run locally in debug mode
> poetry run api --debug

```

These local URI's provide interaction and documentation for the endpoint

* http://127.0.0.1:5000 for root
* http://127.0.0.1:5000/docs for OpenAPI documentation

For testing the HTML template (which can be run without a database, see below), a specific endpoint is provided:

* http://127.0.0.1:5000/test
