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

import unittest

import modelfiles


class TestModels(unittest.TestCase):
    files = [
        "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/.no_exist/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/tokenizer.model",
        "/home/user/.cache/huggingface/hub/models--TheBloke--openinstruct-mistral-7B-GGUF/snapshots/0eda7ce8a5951a2839c32f0bf074eb21dd28ecd8/openinstruct-mistral-7b.Q4_K_M.gguf",
        "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/config.json",
        "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/refs/main",
        "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/snapshots/b5c676eb555d1e44b5381969c7901d31add6673d/smartyplats-7b-v2.Q4_K_M.gguf",
    ]
    def test_filter_models(self):
        m = modelfiles.filter_models(self.files)

        self.assertEqual(2, len(m))
        self.assertEqual("TheBloke/openinstruct-mistral-7B-GGUF", m[0][0])
        self.assertEqual("openinstruct-mistral-7b.Q4_K_M.gguf", m[0][1])
        self.assertEqual("TheBloke/smartyplats-7B-v2-GGUF", m[1][0])
        self.assertEqual("smartyplats-7b-v2.Q4_K_M.gguf", m[1][1])

    def test_model_from_path(self):
        repo, model = modelfiles.model_from_path(
            "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/llama-2-13b-ensemble-v5.Q4_K_M.gguf")
        self.assertEqual("TheBloke/Llama-2-13B-Ensemble-v5-GGUF", repo)
        self.assertEqual("llama-2-13b-ensemble-v5.Q4_K_M.gguf", model)

    def test_model_from_path_unknown_format(self):
        repo, model = modelfiles.model_from_path("foo")
        self.assertEqual("", repo)
        self.assertEqual("", model)

    def test_path_from_repo(self):
        repo_id = "TheBloke/Llama-2-13B-Ensemble-v5-GGUF"
        path = modelfiles.path_from_repo(repo_id)
        self.assertTrue(path.endswith(".cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF"))

    def test_path_from_repo_unknown_format(self):
        path = modelfiles.path_from_repo("SomeRepo")
        self.assertEqual("", path)

    def test_find_model(self):
        model = "smartyplats-7b-v2.Q4_K_M.gguf"
        path = modelfiles.find_model(self.files, model)
        self.assertEqual(
            "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/snapshots/b5c676eb555d1e44b5381969c7901d31add6673d/smartyplats-7b-v2.Q4_K_M.gguf",
            path)


if __name__ == "__main__":
    unittest.main()