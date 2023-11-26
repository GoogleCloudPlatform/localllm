"""Functions for interacting with model files on disk.
"""
import os


MODEL_DIR = "~/.cache/huggingface/hub/"
DEFAULT_FILE_EXT = "gguf"


def get_model_dir():
    return os.path.expanduser(MODEL_DIR)


def list_models():
    """
    List models downloaded to disk
    """
    model_dir = get_model_dir()
    if os.path.isdir(model_dir):
        return filter_models(get_all_files(model_dir))
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


def path_from_repo(repo_id):
    """
    Returns the path the repo would be cached at.
    """
    parts = repo_id.split("/")
    if len(parts) != 2:
        return ""
    return os.path.join(get_model_dir(), "--".join(["models", parts[0], parts[1]]))


def get_all_files(model_dir):
    """
    Returns full path to all files within the directory.
    """
    all_files = []
    for root, _, files in os.walk(os.path.expanduser(model_dir)):
        all_files.extend([os.sep.join([root, f]) for f in files])
    return all_files


def path_from_model(repo_files, model):
    """
    Returns the path the file in the repo is cached at.

    If the file isn't cached, nothing is returned.
    If multiple copies are present, the first one is returned.
    """
    for file in repo_files:
        if file.endswith(model):
            return file
    return ""