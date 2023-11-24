# localllm

Run LLMs locally on Cloud Workstations. Uses:

* Quantized models from 🤗
* [llama-cpp-python's webserver](https://github.com/abetlen/llama-cpp-python#web-server)

## Getting started so far

```bash
python3 -m venv ~/.localllm
source ~/.localllm/bin/activate

# Install the tools
pip3 install -r requirements.txt
pip3 install ./llm-tool/.

# Download the models
llm models download TheBloke/Llama-2-13B-Ensemble-v5-GGUF
llm models download TheBloke/openinstruct-mistral-7B-GGUF

# Host the models (may need to change the snapshot)
python3 -m llama_cpp.server --model ~/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/llama-2-13b-ensemble-v5.Q4_K_M.gguf --host 0.0.0.0 --port 8000
python3 -m llama_cpp.server --model ~/.cache/huggingface/hub/models--TheBloke--openinstruct-mistral-7B-GGUF/snapshots/0eda7ce8a5951a2839c32f0bf074eb21dd28ecd8/openinstruct-mistral-7b.Q4_K_M.gguf --host 0.0.0.0 --port 8001

# Try out some queries
./trylocal.py
```

You can interact with the Open API interface (which will also all you to query the models)
by visiting the `/docs` extenstion, e.g. for the above:

* http://localhost:8000/docs
* http://localhost:8001/docs

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