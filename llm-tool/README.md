# llm tool

A command line tool for interacting with models and offering them via a local API
server. Uses:
* Quantized models from 🤗
* [llama-cpp-python's webserver](https://github.com/abetlen/llama-cpp-python#web-server)

Assumes that models are downloaded to `/models` and only supports `.gguf` files.

## Install

```bash
pip install .
```

## Model management

### List downloaded models

```bash
llm models list
```

### Download a model from 🤗

### Update a model from 🤗

### Remove a model

## Model serving

### Start serving a model

### Stop serving a model

### List model statuses

```bash
llm serving status
```

## Develop

```bash
python3 -m venv .llm
source .llm/bin/activate
pip install --editable .
```

### Test

```bash
python3 -m unittest
```