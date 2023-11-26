# llm tool

A command line tool for interacting with models and offering them via a local API
server. Uses:
* Quantized models from 🤗
* [llama-cpp-python's webserver](https://github.com/abetlen/llama-cpp-python#web-server)

Assumes that models are downloaded to `~/.cache/huggingface/hub/` (the default cache path
used by https://github.com/huggingface/huggingface_hub) and only supports `.gguf` files.

## Install

```bash
pip install .
```

## Model management

### List downloaded models

```bash
llm models list
```

### Download (or update) a model from 🤗

If you're using models from TheBloke we can make some assumptions about repo
structure:

```bash
llm models download TheBloke/Llama-2-13B-Ensemble-v5-GGUF
```

If you want a different specific file in the repo or the repo you are using
doesn't follow the same file naming, you can specify the file explicitly:

```bash
llm models download TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf
```

### Remove a model

To remove a previously downloaded repo:

```bash
llm models rm TheBloke/Llama-2-13B-Ensemble-v5-GGUF
```

To remove a specific file downloaded from a repo:

```bash
llm models rm TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf
```

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