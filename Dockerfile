FROM us-central1-docker.pkg.dev/cloud-workstations-images/predefined/code-oss:latest

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /models
RUN cd /models && wget https://huggingface.co/TheBloke/Llama-2-13B-Ensemble-v5-GGUF/resolve/main/llama-2-13b-ensemble-v5.Q4_K_M.gguf
RUN cd /models && wget https://huggingface.co/TheBloke/openinstruct-mistral-7B-GGUF/resolve/main/openinstruct-mistral-7b.Q4_K_M.gguf
