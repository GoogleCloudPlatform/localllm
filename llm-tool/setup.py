#!/usr/bin/env python

# Copyright 2023 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0

from setuptools import setup

setup(
    name='llm',
    version='0.0.1',
    py_modules=[
        'llm',
        'modeldownload',
        'modelfiles',
        'modelserving',
    ],
    install_requires=[
        'Click',
        'llama-cpp-python[server]',
        'psutil',
        'huggingface_hub'
    ],
    entry_points={
        'console_scripts': [
            'llm = llm:cli',
        ],
    },
)
