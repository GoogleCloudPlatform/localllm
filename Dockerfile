FROM us-central1-docker.pkg.dev/cloud-workstations-images/predefined/code-oss:latest

RUN pip config set global.disable-pip-version-check true
RUN pip install openai --root-user-action=ignore

COPY llm-tool llm-tool
RUN cd llm-tool && pip install --root-user-action=ignore .