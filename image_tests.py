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

"""Test(s) to run from inside the built image
"""
import atexit
import logging
import openai
import os
import shlex
import subprocess
import sys
import time
import unittest


HOST="0.0.0.0"
PORT=8000
LLAMA_REPO="TheBloke/Llama-2-13B-Ensemble-v5-GGUF"
MISTRAL_REPO="TheBloke/openinstruct-mistral-7B-GGUF"

RUN_COMMAND="local-llm run {} {} --verbose"
KILL_COMMAND="local-llm kill {}"


def wait_for_llm(p):
    while True:
        if p.poll() != None:
            return False
        output = p.stdout.readline().decode("utf-8").rstrip()
        if output:
            print(output)
        if "Uvicorn running on" in output:
            return True


def kill_llm(p, model):
    p.kill()
    subprocess.check_call(shlex.split(KILL_COMMAND.format(model)))


class TestLLMs(unittest.TestCase):
    def test_llama(self):
        response = self._test_llm(LLAMA_REPO)
        self.assertNotEqual("", response)

    def test_mistral(self):
        # The mistral model seems to sometimes return empty content for some reason
        _ = self._test_llm(MISTRAL_REPO)

    def _test_llm(self, model):
        command = shlex.split(RUN_COMMAND.format(model, PORT))
        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT) as p:

            # ensure the process is cleaned up even if interrupted
            atexit.register(lambda: kill_llm(p, model))
            if not wait_for_llm(p):
                self.fail(f"Failed to run {' '.join(command)}")

            client = openai.OpenAI(
                api_key="foo",
                base_url=f"http://{HOST}:{PORT}/v1",
            )
            chat_completion = client.chat.completions.create(
                messages=[{
                        "role": "user",
                        "content": "Please write me a haiku about cats",
                }],
                model="",
            )

            kill_llm(p, model)
            self.assertNotEqual(0, len(chat_completion.choices))
            print(chat_completion.choices[0].message.content)
            return chat_completion.choices[0].message.content

    def test_backward_compatible_command(self):
        """Test original command works.

        This was the original command and supported (in the cloud
        workstations image only) for backward compatibility
        """
        subprocess.run("llm")

if __name__ == "__main__":
    unittest.main()
