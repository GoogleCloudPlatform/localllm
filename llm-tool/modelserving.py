#!/usr/bin/python
#
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Serve models locally

Uses https://github.com/abetlen/llama-cpp-python#web-server to serve models
"""
import os
import psutil
import shlex
import subprocess

import modelfiles


COMMAND="uvicorn --factory llama_cpp.server.app:create_app --host {} --port {}"
LOG_COMMAND="--log-config={}"


def running_models():
    """
    Returns a list of models that appear to be currently running
    """
    models = []
    for p in psutil.process_iter([]):
        try:
            env = p.environ()
        except (psutil.AccessDenied, psutil.ZombieProcess):
            continue
        if env.get("RUN_BY_LOCALLLM", "0") == "1":
            model_path = env.get("MODEL", "")
            repo_id, filename = modelfiles.model_from_path(model_path)
            models.append((repo_id, filename, p.pid))
    return models


def start(path, host, port, log_config, verbose):
    """
    Use uvicorn to run lama_cpp.server to start serving the model at path
    running on port at host, using the logging configuration from
    log_config.
    """
    command = shlex.split(COMMAND.format(host, port))
    if log_config != "":
        command.append(LOG_COMMAND.format(log_config))
    env = os.environ.copy()

    # indicate that we started this process so we can easily find it later
    env["RUN_BY_LOCALLLM"] = "1"
    # provide the model to run to llama-cpp-python
    env["MODEL"] = os.path.expanduser(path)
    # stop llama-cpp-python from writing to stderr. we pipe stderr to this
    # process, but then we close the pipe, so subsequent writes to stderr
    # directly fail, causing requests to throw exceptions
    env["VERBOSE"] = "False"

    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env)
    while True:
        if p.poll() != None:
            return False
        output = p.stdout.readline().decode("utf-8").rstrip()
        if output and verbose:
            print(output)
        if "Uvicorn running on" in output:
            return True
    return False
