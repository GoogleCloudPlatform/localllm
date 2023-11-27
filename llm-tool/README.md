# llm tool

A command line tool for interacting with models and offering them via a local API
server. Uses:
* Quantized models from 🤗
* [llama-cpp-python's webserver](https://github.com/abetlen/llama-cpp-python#web-server)

See [../README.md#llm-commands](../README.md#llm-commands) for more examples.

## Install

```bash
pip install .
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