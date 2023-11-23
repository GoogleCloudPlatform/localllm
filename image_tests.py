"""Test(s) to run from inside the built image
"""
import atexit
import logging
import openai
import shlex
import subprocess
import sys
import time
import unittest


HOST="0.0.0.0"
PORT=8000
LLAMA_MODEL= "/models/llama-2-13b-ensemble-v5.Q4_K_M.gguf"
MISTRAL_MODEL= "/models/openinstruct-mistral-7b.Q4_K_M.gguf"
COMMAND="python3 -m llama_cpp.server --model {} --host {} --port {}"


def wait_for_llm(p):
    while True:
        if p.poll() != None:
            return False
        output = p.stdout.readline().decode("utf-8").rstrip()
        if "Uvicorn running on" in output:
            return True


class TestLLMs(unittest.TestCase):
    def test_llama(self):
        self._test_llm(LLAMA_MODEL)

    def test_mistral(self):
        self._test_llm(MISTRAL_MODEL)

    def _test_llm(self, model):
        with subprocess.Popen(
            shlex.split(COMMAND.format(model, HOST, PORT)),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT) as p:

            # ensure the process is cleaned up even if interrupted
            atexit.register(lambda: p.kill())
            self.assertTrue(wait_for_llm(p))

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
            # TODO: the mistral model did sometimes return empty content, this might have false negatives
            self.assertNotEqual("", chat_completion.choices[0].message.content)


if __name__ == "__main__":
    unittest.main()
