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

"""A command line tool for interacting with local models
"""
import click
import psutil

import modelfiles
import modelserving
import modeldownload


MODEL_STR = "\t{} {}"


@click.group()
def cli():
    """Download and run local LLMs from 🤗"""


@cli.command()
def list():
    """List the locally cached models"""
    m = modelfiles.list_models()
    click.echo(f"Models installed to {modelfiles.get_model_dir()}...")
    for mm in m:
        click.echo(MODEL_STR.format(mm[0], mm[1]))


def _pull(repo_id, filename):
    click.echo(f"Pulling {filename} from {repo_id}")
    path = modeldownload.download(repo_id, filename)
    click.echo(f"Pulled to {path}")
    return path


@cli.command()
@click.argument("repo_id")
@click.option("--filename", default="",
              help="The specific model file to download. Will assume 4 bit medium model if not provided")
def pull(repo_id, filename):
    """Download model from REPO_ID at 🤗"""
    filename = modeldownload.default_filename(repo_id) if not filename else filename
    if not filename:
        click.echo(f"Unable to determine filename to use for {repo_id}.")
        exit(1)
    _pull(repo_id, filename)


@cli.command()
@click.argument("repo_id")
@click.option("--filename", default="",
              help="The specific file to download. Will delete entire repo if not provided.")
def rm(repo_id, filename):
    """Delete REPO_ID from disk or a specific file within a repo"""
    click.echo(f"Removing {filename} from {repo_id}")
    path = modeldownload.remove(repo_id, filename)
    if path:
        click.echo(f"Removed {path}")
    else:
        click.echo("Nothing to remove")


@cli.command()
@click.argument("repo_id")
@click.option("--host", default="0.0.0.0")
@click.argument("port")
@click.option("--filename", default="", help="The specific file to run.")
@click.option("--log-config", envvar="LOG_CONFIG", default="",
              help="The logging configuration to pass to uvicorn.")
@click.option('--verbose/--no-verbose', default=False)
def run(repo_id, host, port, filename, log_config, verbose):
    """Start running the specified model. Downloads if not already present."""
    filename = modeldownload.default_filename(repo_id) if not filename else filename
    path = modelfiles.path_from_model(repo_id, filename)
    if not path:
        path = _pull(repo_id, filename)
    if not modelserving.start(path, host, port, log_config, verbose):
        click.echo("Error starting LLM, run with --verbose for more")
        exit(1)
    else:
        click.echo(f"Running {path} at {host}:{port}")


@cli.command()
@click.argument("repo_id")
@click.option("--filename", default="", help="The specific file to run.")
def kill(repo_id, filename):
    """Kill running models, either filename from repo_id or instances of models from repo_id."""
    m = modelserving.running_models()
    for m_repo_id, m_filename, m_pid in m:
        if m_repo_id == repo_id:
            if not filename or m_filename == filename:
                click.echo(f"Killing {m_repo_id}:{m_filename} at {m_pid}")
                psutil.Process(m_pid).kill()



@cli.command()
def ps():
    """Return all the cached models currently running via llama_cpp.server
    """
    m = modelserving.running_models()
    if len(m) > 0:
        click.echo(f"Models in {modelfiles.get_model_dir()} currently running...")
        for mm in m:
            click.echo(MODEL_STR.format(mm[0], mm[1]))
    else:
        click.echo("No models currently running.")
