FROM us-central1-docker.pkg.dev/cloud-workstations-images/predefined/code-oss:latest

RUN pip config set global.disable-pip-version-check true
RUN pip install openai --root-user-action=ignore

COPY local-llm local-llm
RUN cd local-llm && pip install --root-user-action=ignore .
# Support the original name of the cli tool as well as the latest version(s)
RUN ln -s $(which local-llm) /usr/local/bin/llm

# Startup script will setup log files
COPY workstation-startup.d/* /etc/workstation-startup.d/

# configure the location of the local-llm log configuration
COPY local-llm/log_config.yaml /etc/local-llm_log_config.yaml
ENV LOG_CONFIG="/etc/local-llm_log_config.yaml"