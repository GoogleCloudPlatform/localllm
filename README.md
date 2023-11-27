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
llm serving run TheBloke/Llama-2-13B-Ensemble-v5-GGUF 0.0.0.0 8000

# Try out a queries
./querylocal.py
```

You can interact with the Open API interface (which will also all you to query the models)
by visiting the `/docs` extenstion, e.g. for the above:

* http://localhost:8000/docs

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