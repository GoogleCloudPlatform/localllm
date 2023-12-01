# localllm

Run LLMs locally on Cloud Workstations. Uses:

- Quantized models from 🤗
- [llama-cpp-python's webserver](https://github.com/abetlen/llama-cpp-python#web-server)

## Try it out locally

```bash
# Install the tools
pip3 install openai
pip3 install ./llm-tool/.

# Download and run a model
llm run TheBloke/Llama-2-13B-Ensemble-v5-GGUF 8000

# Try out a query
./querylocal.py
```

You can interact with the Open API interface by visiting the `/docs` extenstion, e.g. for the above: http://localhost:8000/docs

## Running on [Cloud Workstation](https://cloud.google.com/workstations)

This repository includes a [Dockerfile](./Dockerfile) that can be used to create a [custom base image](https://cloud.google.com/workstations/docs/customize-container-images) for a Cloud Workstation environment that includes the `llm` tool.

To get started, you'll need to have a [GCP Project](https://cloud.google.com/docs/get-started) and have the [`gcloud` CLI installed](https://cloud.google.com/sdk/docs/install).

```
gcloud config set project $PROJECT_ID

# Enable needed services
gcloud services enable \
  cloudbuild.googleapis.com \
  workstations.googleapis.com \
  container.googleapis.com \
  containeranalysis.googleapis.com \
  containerscanning.googleapis.com \
  artifactregistry.googleapis.com

# Create AR Docker repository
gcloud artifacts repositories create localllm \
  --location=us-central1 \
  --repository-format=docker
```

Next, submit a build of the Dockerfile, which will also push the image to Artifact Registry.

```bash
gcloud builds submit .
```

The published image is named `us-central1-docker.pkg.dev/$PROJECT_ID/localllm/localllm`.

The next step is to [create and launch a workstation](https://cloud.google.com/workstations/docs/create-workstation)
using our custom image. We suggest using a machine type of e2-standard-32 (32 vCPU, 16 core and 128 GB memory).

The following example uses `gcloud` to configure a cluster, configuration and workstation using our custom
base image with `llm` installed. Replace `$CLUSTER` with your desired cluster name, and the command
below will create a new one (which takes ~20 minutes).

```bash
gcloud workstations clusters create $CLUSTER \
  --region=us-central1
```

The next steps create the workstation, and starts it up. These steps will take ~10 minutes to run.

```bash
# Create workstation configuration
gcloud workstations configs create localllm-workstation \
  --region=us-central1 \
  --cluster=$CLUSTER \
  --machine-type=e2-standard-32 \
  --container-custom-image=us-central1-docker.pkg.dev/$PROJECT_ID/localllm/localllm

# Create the workstation
gcloud workstations create locallm-workstation \
  --cluster=$CLUSTER \
  --config=localllm-workstation \
  --region=us-central1

# Grant access to the default Cloud Workstation Service Account
gcloud artifacts repositories add-iam-policy-binding \
  localllm \
  --location=us-central1 \
  --member=serviceAccount:service-$PROJECT_NUM@gcp-sa-workstationsvm.iam.gserviceaccount.com \
  --role=roles/artifactregistry.reader

# Start the workstation
gcloud workstations start locallm-workstation \
  --cluster=$CLUSTER \
  --config=localllm-workstation \
  --region=us-central1
```

You can connect to the workstation using ssh (shown below), or [interactively](https://cloud.google.com/workstations/docs/create-workstation#launch_a_workstation) in the browser.

```bash
gcloud workstations ssh locallm-workstation \
  --cluster=$CLUSTER \
  --config=localllm-workstation \
  --region=us-central1
```

After serving a model (see `llm run` below, noting the `$PORT` used for serving), you can interact with 
the model by visiting the live OpenAPI documentation page. First, get the hostname of the workstation using:

```bash
gcloud workstations describe locallm-workstation \
  --cluster=$CLUSTER \
  --config=localllm-workstation \
  --region=us-central1
```

Then, in the browser, visit `https://$PORT-$HOSTNAME/docs`.

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

## LLM Disclaimer

This project imports freely available LLMs and makes them available from [Cloud Workstations](https://cloud.google.com/workstations). We recommend independently verifying any content generated by the models.
We do not assume any responsibility or liability for the use or interpretation of generated content.
