"""Serve models locally

Uses https://github.com/abetlen/llama-cpp-python#web-server to serve models
"""
import psutil

import modelfiles


def running_models():
    """
    Returns a list of models that appear to be currently running
    """
    procs = [proc.cmdline() for proc in psutil.process_iter([])]
    return filter_running_models(procs)


def filter_running_models(processes):
    """
    Returns the list of running models
    """
    models = []
    for p in processes:
        if len(p) == 0:
            continue
        if p[0].startswith("python"):
            for i, arg in enumerate(p):
                if arg == "--model":
                    if len(p) < i+2:
                        continue
                    models.append(modelfiles.model_from_path(p[i+1]))
    return models
