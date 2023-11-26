"""A command line tool for interacting with local models
"""
import click


import modelfiles
import modelserving
import modeldownload


MODEL_STR = "\t{}:{}"


@click.group()
def cli():
    """Download and run local LLMs"""


@cli.group()
def models():
    """Interact with models on 🤗 and on disk"""


@models.command()
def list():
    """List the locally cached models"""
    m = modelfiles.list_models()
    click.echo(f"Models installed to {modelfiles.get_model_dir()}...")
    for mm in m:
        click.echo(MODEL_STR.format(mm[0], mm[1]))


@models.command()
@click.argument("repo_id")
@click.option("--filename", default="",
              help="The specific model file to download. Will assume 4 bit medium model if not provided")
def download(repo_id, filename):
    """Download model from REPO_ID at 🤗"""
    filename = modeldownload.default_filename(repo_id) if not filename else filename
    if not filename:
        click.echo(f"Unable to determine filename to use for {repo_id}.")
        exit(1)
    click.echo(f"Downloading {filename} from {repo_id}")
    path = modeldownload.download(repo_id, filename)
    click.echo(f"Downloaded to {path}")


@models.command()
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


@cli.group()
def serving():
    """Serve models locally"""


@serving.command()
def start():
    click.echo("START")


@serving.command()
def stop():
    click.echo("STOP")


@serving.command()
def status():
    """Return all the cached models currently running via llama_cpp.server
    """
    m = modelserving.running_models()
    if len(m) > 0:
        click.echo(f"Models in {modelfiles.get_model_dir()} currently running...")
        for mm in m:
            click.echo(MODEL_STR.format(mm[0], mm[1]))
    else:
        click.echo("No models currently running.")
