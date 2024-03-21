#!/usr/bin/python
#
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

setup(
    name='local-llm',
    version='0.0.1',
    py_modules=[
        'local_llm',
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
            'local-llm = local_llm:cli',
        ],
    },
    package_data = {
        "": ["local-llm_log_config.yaml"],
    }
)