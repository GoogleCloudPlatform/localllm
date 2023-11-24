"""Serve models locally

Uses https://github.com/abetlen/llama-cpp-python#web-server to serve models
"""
import psutil


def running_models(models):
    """
    Returns a list of models that appear to be currently running
    """
    procs = [proc.cmdline() for proc in psutil.process_iter([])]
    running = []
    for model in models:
        if is_running(model, procs):
            running.append(model)
    return running


def is_running(model, processes):
    """
    Returns true if a python process is running the model
    """
    for p in processes:
        if len(p) == 0:
            continue
        if p[0].startswith("python"):
            for i, arg in enumerate(p):
                if arg == "--model":
                    if len(p) < i+2:
                        continue
                    if model in p[i+1]:
                        return True
    return False
