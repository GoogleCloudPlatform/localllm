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

import sys


def main(argv):
    pass


if __name__ == '__main__':
    main(sys.argv)
"""Serve models locally

Uses https://github.com/abetlen/llama-cpp-python#web-server to serve models
"""
import os
import psutil
import shlex
import subprocess

import modelfiles


COMMAND="python3 -m llama_cpp.server --model {} --host {} --port {}"


def running_models():
    """
    Returns a list of models that appear to be currently running
    """
    procs = [(proc.cmdline(), proc.pid) for proc in psutil.process_iter([])]
    return filter_running_models(procs)


def filter_running_models(processes):
    """
    Returns the list of running models
    """
    models = []
    for p in processes:
        cmdline, pid = p[0], p[1]
        if len(cmdline) == 0:
            continue
        if cmdline[0].startswith("python"):
            for i, arg in enumerate(cmdline):
                if arg == "--model":
                    if len(cmdline) < i+2:
                        continue
                    repo_id, filename = modelfiles.model_from_path(cmdline[i+1])
                    models.append((repo_id, filename, pid))

    return models


def start(path, host, port, verbose):
    """
    Use lama_cpp.server to start serving the model at path.
    """
    command = shlex.split(COMMAND.format(os.path.expanduser(path), host, port))
    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    while True:
        if p.poll() != None:
            return False
        output = p.stdout.readline().decode("utf-8").rstrip()
        if output and verbose:
            print(output)
        if "Uvicorn running on" in output:
            return True
    return False
