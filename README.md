# localllm

Run LLMs locally on Cloud Workstations. Uses:

* Quantized models from 🤗
* [llama-cpp-python's webserver](https://github.com/abetlen/llama-cpp-python#web-server)

## Try it out

```bash
# Install the tools
pip3 install openai
pip3 install ./llm-tool/.

# Download and run a model
llm run TheBloke/Llama-2-13B-Ensemble-v5-GGUF 0.0.0.0 8000

# Try out a queries
./querylocal.py
```

You can interact with the Open API interface by visiting the `/docs` extenstion, e.g. for the above: http://localhost:8000/docs

## llm commands

Assumes that models are downloaded to `~/.cache/huggingface/hub/` (the default cache path
used by https://github.com/huggingface/huggingface_hub) and only supports `.gguf` files.

If you're using models from TheBloke and you don't specify a filename, we'll attempt to use
the model with 4 bit medium quantization, or you can specify a filename explicitly.


```bash
# List downloaded models
llm list

# List running models
llm ps

# Start serving the default model from the repo (download if not present)
llm run TheBloke/Llama-2-13B-Ensemble-v5-GGUF 8000
# Start serving a specific model (download if not present)
llm run TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf 8000

# Stop serving all models from the repo
llm kill TheBloke/Llama-2-13B-Ensemble-v5-GGUF
# Stop serving a specific model
llm kill TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf

# Download the default model from the repo
llm pull TheBloke/Llama-2-13B-Ensemble-v5-GGUF
# Download a specific model from the repo
llm pull TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf

# Remove all models downloaded from the repo
llm rm TheBloke/Llama-2-13B-Ensemble-v5-GGUF
# Remove a specific model
llm rm TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf
```

## Running cloud workstation

Currently using:
* e2-standard-32 (32 vCPU, 16 core, 128 GB memory)
* `us-central1-docker.pkg.dev/cloud-workstations-images/predefined/code-oss:latest`

## Image publishing

GCB automation publishes to `us-central1-docker.pkg.dev/$PROJECT_ID/localllm`. Enable GCR
(including image vulnerability scanning and provenance generation) and create the image
repo with:

```
gcloud config set project $PROJECT_ID
gcloud services enable \
  container.googleapis.com \
  containeranalysis.googleapis.com \
  containerscanning.googleapis.com \
  artifactregistry.googleapis.com

gcloud artifacts repositories create localllm \
  --location=us-central1 \
  --repository-format=docker \
  --project=$PROJECT_ID
```

The published image is called `us-central1-docker.pkg.dev/$PROJECT_ID/localllm/localllm-cw`.