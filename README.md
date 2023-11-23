# localllm

Run LLMs locally on Cloud Workstations. Uses:

* Quantized models from HuggingFace
* [llama-cpp-python's webserver](https://github.com/abetlen/llama-cpp-python#web-server)

## Getting started so far

```bash
python3 -m venv ~/.localllm
source ~/.localllm/bin/activate
pip3 install -r requirements.txt

wget https://huggingface.co/TheBloke/Llama-2-13B-Ensemble-v5-GGUF/resolve/main/llama-2-13b-ensemble-v5.Q4_K_M.gguf
wget https://huggingface.co/TheBloke/openinstruct-mistral-7B-GGUF/resolve/main/openinstruct-mistral-7b.Q4_K_M.gguf

python3 -m llama_cpp.server --model llama-2-13b-ensemble-v5.Q4_K_M.gguf --host 0.0.0.0 --port 8000
python3 -m llama_cpp.server --model openinstruct-mistral-7b.Q4_K_M.gguf --host 0.0.0.0 --port 8001
```

Try it out with the script (from the virtual env ^^):

```bash
(.localllm) ./trylocal.py
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


## TODO

1. Grab the latest version of each model instead of hardcoding
2. Any way to increase ulimit or limited by cloud workstations container?

https://github.com/abetlen/llama-cpp-python/issues/254

```
INFO     image_tests:image_tests.py:27 warning: failed to mlock 92168192-byte buffer (after previously locking 0 bytes): Cannot allocate memory
INFO     image_tests:image_tests.py:27 Try increasing RLIMIT_MLOCK ('ulimit -l' as root).
```

3. The base image has 176 vulnerabilities :( Running `apt full-upgrade` removed 15 only 🙃

