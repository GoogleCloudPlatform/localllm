FROM us-central1-docker.pkg.dev/cloud-workstations-images/predefined/code-oss:latest

RUN pip config set global.disable-pip-version-check true
RUN pip install openai --root-user-action=ignore

COPY llm-tool llm-tool
RUN cd llm-tool && pip install --root-user-action=ignore .

# Startup script will setup log files
COPY workstation-startup.d/* /etc/workstation-startup.d/

# configure the location of the localllm log configuration
COPY llm-tool/llm_log_config.yaml /etc/llm_log_config.yaml
ENV LOG_CONFIG="/etc/llm_log_config.yaml"