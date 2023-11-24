#!/bin/bash

# move the model files downloaded into the https://github.com/huggingface/huggingface_hub 
# cache from the root user to the cloud workstation user
# e.g. /root/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/llama-2-13b-ensemble-v5.Q4_K_M.gguf 
mkdir /home/user/.cache/
mv /root/.cache/huggingface /home/user/.cache/
chown -R user:user /home/user/.cache