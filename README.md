# localllm

Run LLMs locally on Cloud Workstations. Uses:

- Quantized models from 🤗
- [llama-cpp-python's webserver][web-server]

## Running locally

1. Install the tools.

```shell
# Install the tools
pip3 install openai
pip3 install ./llm-tool/.
```

2. Download and run a model.

```shell
llm run TheBloke/Llama-2-13B-Ensemble-v5-GGUF 8000
```

3. Try out a query. The default query is for a haiku about cats.

```shell
python3 querylocal.py
```

4. Interact with the Open API interface via the `/docs` extension. For the above, visit http://localhost:8000/docs. 

## Running on [Cloud Workstation][cw]

This repository includes a [Dockerfile](./Dockerfile) that can be used to create a [custom base image][cw-custom] 
for a Cloud Workstation environment that includes the `llm` tool.

To get started, you'll need to have a [GCP Project][gcp] and have the `gcloud` CLI [installed][gcloud].

1. Set environment variables
   1. Set the `PROJECT_ID` and `PROJECT_NUM` environment variables from your GCP project. You must modify the values.

   ```shell
   export PROJECT_ID=<project-id>
   export PROJECT_NUM=<project-num>
   ```
   
   2. Set other needed environment variables. You can modify the values.
   ```shell
   export REGION=us-central1
   export LOCALLLM_REGISTRY=localllm-registry
   export LOCALLLM_CLUSTER=localllm-cluster
   export LOCALLLM_WORKSTATION=localllm-workstation
   export LOCALLLM_PORT=8000
   ```

2. Set the default project.

```shell
gcloud config set project $PROJECT_ID
```

3. Enable needed services.

```shell
gcloud services enable \
  cloudbuild.googleapis.com \
  workstations.googleapis.com \
  container.googleapis.com \
  containeranalysis.googleapis.com \
  containerscanning.googleapis.com \
  artifactregistry.googleapis.com
```

4. Create an Artifact Registry repository for docker images.

```shell
gcloud artifacts repositories create $LOCALLLM_REGISTRY \
  --location=$REGION \
  --repository-format=docker
```

5. Build and push the image to Artifact Registry using Cloud Build. Details are in [cloudbuild.yaml](cloudbuild.yaml).
   The published image is `us-central1-docker.pkg.dev/$PROJECT_ID/localllm/localllm`.

```shell
gcloud builds submit .
```

7. Configure a Cloud Workstation cluster.

```shell
gcloud workstations clusters create $LOCALLLM_CLUSTER \
  --region=$REGION
```

8. Create a Cloud Workstation configuration. We suggest using a machine type of e2-standard-32 which has 32 vCPU, 16 
   core and 128 GB memory.

```shell
gcloud workstations configs create $LOCALLLM_WORKSTATION \
--region=$REGION \
--cluster=$LOCALLLM_CLUSTER \
--machine-type=e2-standard-32 \
--container-custom-image=us-central1-docker.pkg.dev/$PROJECT_ID/localllm/localllm
```

9. Create a Cloud Workstation.

```shell
gcloud workstations create $LOCALLLM_WORKSTATION \
--cluster=$LOCALLLM_CLUSTER \
--config=$LOCALLLM_WORKSTATION \
--region=$REGION
```

10. Grant access to the default Cloud Workstation service account.

```shell
gcloud artifacts repositories add-iam-policy-binding $LOCALLLM_REGISTRY \
  --location=$REGION \
  --member=serviceAccount:service-$PROJECT_NUM@gcp-sa-workstationsvm.iam.gserviceaccount.com \
  --role=roles/artifactregistry.reader
```

11. Start the workstation.

```shell
gcloud workstations start $LOCALLLM_WORKSTATION \
  --cluster=$LOCALLLM_CLUSTER \
  --config=$LOCALLLM_WORKSTATION \
  --region=$REGION
```

12. Connect to the workstation using ssh. Alternatively, you can connect to the workstation
   [interactively][launch-workstation] in the browser.

```bash
gcloud workstations ssh $LOCALLLM_WORKSTATION \
  --cluster=$LOCALLLM_CLUSTER \
  --config=$LOCALLLM_WORKSTATION \
  --region=$REGION
```

13. Start serving the default model from the repo.

```shell
llm run TheBloke/Llama-2-13B-Ensemble-v5-GGUF $LOCALLLM_PORT
```

14. Get the hostname of the workstation using:

```bash
gcloud workstations describe $LOCALLLM_WORKSTATION \
  --cluster=$LOCALLLM_CLUSTER \
  --config=$LOCALLLM_WORKSTATION \
  --region=$REGION
```

15. Interact with the model by visiting the live OpenAPI documentation page: `https://$LOCALLLM_PORT-$LLM_HOSTNAME/docs`.

## llm commands

Assumes that models are downloaded to `~/.cache/huggingface/hub/`. This is the default cache
path used by Hugging Face Hub [library][hf-hub] and only supports `.gguf` files.

If you're using models from TheBloke and you don't specify a filename, we'll attempt to use
the model with 4 bit medium quantization, or you can specify a filename explicitly.

1. List downloaded models.

```shell
llm list
```

2. List running models. 

```shell
llm ps
```

3. Start serving models.

   1. Start serving the default model from the repo. Download if not present.

   ```shell
   llm run TheBloke/Llama-2-13B-Ensemble-v5-GGUF 8000
   ```

   2. Start serving a specific model. Download if not present.

   ```shell
   llm run TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf 8000
   ```

4. Stop serving models.

   1. Stop serving all models from the repo.

   ```shell
   llm kill TheBloke/Llama-2-13B-Ensemble-v5-GGUF
   ```

   2. Stop serving a specific model.

   ```shell
   llm kill TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf
   ```

5. Download models.

   1. Download the default model from the repo. 

   ```shell
   llm pull TheBloke/Llama-2-13B-Ensemble-v5-GGUF
   ```
   2. Download a specific model from the repo.

   ```shell
   llm pull TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf
   ```

6. Remove models.

   1. Remove all models downloaded from the repo.

   ```shell
   llm rm TheBloke/Llama-2-13B-Ensemble-v5-GGUF
   ```
   2. Remove a specific model from the repo.

   ```shell
   llm rm TheBloke/Llama-2-13B-Ensemble-v5-GGUF --filename llama-2-13b-ensemble-v5.Q4_K_S.gguf
   ```

## LLM Disclaimer

This project imports freely available LLMs and makes them available from [Cloud Workstations][cw]. We recommend
independently verifying any content generated by the models. We do not assume any responsibility or liability for
the use or interpretation of generated content.

[gcp]: https://cloud.google.com/docs/get-started
[gcloud]: https://cloud.google.com/sdk/docs/install
[cw]: https://cloud.google.com/workstations
[cw-custom]: https://cloud.google.com/workstations/docs/customize-container-images
[launch-workstation]: https://cloud.google.com/workstations/docs/create-workstation#launch_a_workstation
[hf-hub]: https://github.com/huggingface/huggingface_hub
[web-server]: https://github.com/abetlen/llama-cpp-python#web-server
