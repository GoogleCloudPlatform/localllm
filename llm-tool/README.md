# llm tool

A command line tool for interacting with models and offering them via a local API
server. Uses:
* Quantized models from 🤗
* [llama-cpp-python's webserver](https://github.com/abetlen/llama-cpp-python#web-server)

Assumes that models are downloaded to `~/.cache/huggingface/hub/` (the default cache path
used by https://github.com/huggingface/huggingface_hub) and only supports `.gguf` files.

If you're using models from TheBloke and you don't specify a filename, we'll attempt to use
the model with 4 bit medium quantization, or you can specify a filename explicitly.

## Install

```bash
pip install .
```

## List downloaded models

```bash
llm list
```

## Download (or update) a model from 🤗

```bash
# Download the default model from the repo
llm pull TheBloke/Llama-2-13B-Ensemble-v5-GGUF

# Download a specific model from the repo
llm pull TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf
```

## Remove a model

```bash
# Remove all models downloaded from the repo
llm rm TheBloke/Llama-2-13B-Ensemble-v5-GGUF

# Remove a specific model
llm rm TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf
```

## Start serving a model

Will download if not already present.

```bash
# Start serving the default model from the repo
llm run TheBloke/Llama-2-13B-Ensemble-v5-GGUF 8000

# Start serving a specific model
llm run TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf 8000
```

## Stop serving a model

```bash
# Stop serving all models from the repo
llm kill TheBloke/Llama-2-13B-Ensemble-v5-GGUF

# Stop serving a specific model
llm kill TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf
```

## List running models

```bash
llm ps
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