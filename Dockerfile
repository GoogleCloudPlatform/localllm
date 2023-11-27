FROM us-central1-docker.pkg.dev/cloud-workstations-images/predefined/code-oss:latest

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY llm-tool llm-tool
RUN cd llm-tool && pip install .

RUN llm pull TheBloke/Llama-2-13B-Ensemble-v5-GGUF
RUN llm pull TheBloke/openinstruct-mistral-7B-GGUF

# Startup script will move downloaded models from root home cache to user's cache
COPY workstation-startup.d/* /etc/workstation-startup.d/