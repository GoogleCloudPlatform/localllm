FROM us-central1-docker.pkg.dev/cloud-workstations-images/predefined/code-oss:latest

RUN pip install openai

COPY llm-tool llm-tool
RUN cd llm-tool && pip install .