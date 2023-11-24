"""A command line tool for interacting with local models
"""
import click


import modelfiles
import modelserving
import modeldownload


@click.group()
def cli():
    """Download and run local LLMs"""
    if not modelfiles.dir_exists():
        click.echo(f"Model directory {modelfiles.MODEL_DIR} does not exist. Please create it.")
        exit(1)


@cli.group()
def models():
    """Interact with models on 🤗 and on disk"""
    pass


@models.command()
def list():
    m = modelfiles.list()
    click.echo(f"Models installed to {modelfiles.MODEL_DIR}...")
    for mm in m:
        click.echo(f"\t{mm}")


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
def update():
    click.echo("UPDATE")


@models.command()
def remove():
    click.echo("REMOVE")


@cli.group()
def serving():
    pass


@serving.command()
def start():
    click.echo("START")


@serving.command()
def stop():
    click.echo("STOP")


@serving.command()
def status():
    m = modelserving.running_models(modelfiles.list())
    if len(m) > 0:
        click.echo(f"Models in {modelfiles.MODEL_DIR} currently running...")
        for mm in m:
            click.echo(f"\t{mm}")
    else:
        click.echo("No models currently running.")
