"""Functions for interacting with model files on disk.
"""
import os


MODEL_DIR = "~/.cache/huggingface/hub/"
DEFAULT_FILE_EXT = "gguf"


def list_models():
    """
    List models downloaded to disk
    """
    model_dir = os.path.expanduser(MODEL_DIR)
    if os.path.isdir(model_dir):
        models = []
        for root, _, files in os.walk(model_dir):
            models.extend(filter_models([os.sep.join([root, f]) for f in files]))
        return models
    return []


def filter_models(files):
    """
    Returns only the files in the list that appear to be models
    """
    models = []
    for file in files:
        if file.endswith(f".{DEFAULT_FILE_EXT}"):
            repo, model = model_from_path(file)
            if repo != "" and model != "":
                models.append((repo, model))
    return models


def model_from_path(path):
    """
    Returns the 🤗 model repo based on the cached path
    """
    path_parts = path.split(os.sep)
    for p in path_parts:
        parts = p.split("--")
        if len(parts) != 3 or parts[0] != "models":
            continue
        return "/".join(parts[1:]), path_parts[-1]
    return "", ""