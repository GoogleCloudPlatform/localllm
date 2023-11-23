"""A command line tool for interacting with local models
"""
import click


import modelfiles
import modelserving


@click.group()
def cli():
    pass


@cli.group()
def models():
    pass


@models.command()
def list():
    m = modelfiles.list()
    click.echo(f"Models installed to {modelfiles.MODEL_DIR}...")
    for mm in m:
        click.echo(f"\t{mm}")


@models.command()
def download():
    click.echo("DOWNLOAD")


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
