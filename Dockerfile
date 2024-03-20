FROM us-central1-docker.pkg.dev/cloud-workstations-images/predefined/code-oss:latest

RUN pip config set global.disable-pip-version-check true
RUN pip install openai --root-user-action=ignore

COPY localllm localllm
RUN cd localllm && pip install --root-user-action=ignore .
# Support the original name of the cli tool as well as the latest version(s)
RUN ln -s $(which localllm) /usr/local/bin/llm

# Startup script will setup log files
COPY workstation-startup.d/* /etc/workstation-startup.d/

# configure the location of the localllm log configuration
COPY localllm/log_config.yaml /etc/localllm_log_config.yaml
ENV LOG_CONFIG="/etc/localllm_log_config.yaml"