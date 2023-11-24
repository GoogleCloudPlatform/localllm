FROM us-central1-docker.pkg.dev/cloud-workstations-images/predefined/code-oss:latest

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY llm-tool llm-tool
RUN cd llm-tool && pip install .

# hoisted on my petard (not actually using this dir now but still checking for it...)
RUN mkdir /models

RUN llm models download TheBloke/Llama-2-13B-Ensemble-v5-GGUF
RUN llm models download TheBloke/openinstruct-mistral-7B-GGUF
