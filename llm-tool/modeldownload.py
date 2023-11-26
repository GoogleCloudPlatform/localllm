"""Downloads models from 🤗
"""
import huggingface_hub
import os
import shutil

import modelfiles


# Defaulting to 4 bit medium quantization
DEFAULT_QUANT = "Q4_K_M"


def default_filename(repo_id):
    """Returns the default file to look for in that 🤗 repo

    Naming doesn't seem to be consistent across 🤗 but it does seem
    to be consistent across TheBloke's repos, so making some assumptions.
    """
    parts = repo_id.split("/")
    if len(parts) != 2:
        return ""
    model_parts = parts[1].lower().split("-")
    if model_parts[-1] != modelfiles.DEFAULT_FILE_EXT:
        return ""
    model = "-".join(model_parts[:-1])
    return ".".join([model, DEFAULT_QUANT, modelfiles.DEFAULT_FILE_EXT])


def download(repo_id, filename):
    """Downloads file from the path at 🤗

    Uses huggingface_hub library to create a cache.
    """
    return huggingface_hub.hf_hub_download(
        repo_id=repo_id,
        filename=filename,
    )


def remove(repo_id, filename):
    """Removes models from disk

    Either removes entire repo_id or just filename within that repo.
    Does nothing if the file or repo does not exist on disk.
    """
    path = ""
    if filename:
        model_path = modelfiles.path_from_repo(repo_id)
        repo_files = modelfiles.get_all_files(model_path)
        path = modelfiles.path_from_model(repo_files, filename)
        if path:
            os.remove(path)
    if not filename:
        path = modelfiles.path_from_repo(repo_id)
        if path:
            shutil.rmtree(path)
    return path