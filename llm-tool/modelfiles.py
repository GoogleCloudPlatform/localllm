"""Functions for interacting with model files on disk.
"""
import os


MODEL_DIR = "/models"
SUPPORTED_EXTS = [".gguf"]


def list():
    """
    List models downloaded to disk
    """
    return filter_models(os.listdir(MODEL_DIR))


def filter_models(files):
    """
    Returns only the files in the list that appear to be models
    """
    models = []
    for file in files:
        parts = os.path.splitext(file)
        if len(parts) != 2:
            continue
        if parts[1] in SUPPORTED_EXTS:
            models.append(file)
    return models
