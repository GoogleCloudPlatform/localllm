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
LLAMA_MODEL="~/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/llama-2-13b-ensemble-v5.Q4_K_M.gguf"
MISTRAL_MODEL="~/.cache/huggingface/hub/models--TheBloke--openinstruct-mistral-7B-GGUF/snapshots/0eda7ce8a5951a2839c32f0bf074eb21dd28ecd8/openinstruct-mistral-7b.Q4_K_M.gguf"

COMMAND="python3 -m llama_cpp.server --model {} --host {} --port {}"


def wait_for_llm(p):
    while True:
        if p.poll() != None:
            return False
        output = p.stdout.readline().decode("utf-8").rstrip()
        if output:
            print(output)
        if "Uvicorn running on" in output:
            return True


class TestLLMs(unittest.TestCase):
    def test_llama(self):
        response = self._test_llm(LLAMA_MODEL)
        self.assertNotEqual("", response)

    def test_mistral(self):
        # The mistral model seems to sometimes return empty content for some reason
        _ = self._test_llm(MISTRAL_MODEL)

    def _test_llm(self, model):
        command = shlex.split(COMMAND.format(os.path.expanduser(model), HOST, PORT))
        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT) as p:

            # ensure the process is cleaned up even if interrupted
            atexit.register(lambda: p.kill())
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

            p.kill()
            self.assertNotEqual(0, len(chat_completion.choices))
            print(chat_completion.choices[0].message.content)
            return chat_completion.choices[0].message.content


if __name__ == "__main__":
    unittest.main()
