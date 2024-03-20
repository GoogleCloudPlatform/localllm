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

import modeldownload


class TestModelDownload(unittest.TestCase):
    def test_default_filename(self):
        repo_id = "TheBloke/Llama-2-13B-Ensemble-v5-GGUF"
        filename = modeldownload.default_filename(repo_id)
        self.assertEqual("llama-2-13b-ensemble-v5.Q4_K_M.gguf", filename)

    def test_default_filename_unknown_format(self):
        filename = modeldownload.default_filename("foo")
        self.assertEqual("", filename)

    def test_default_filename_unsupported_ext(self):
        repo_id = "TheBloke/openinstruct-mistral-7B-GPTQ"
        filename = modeldownload.default_filename(repo_id)
        self.assertEqual("", filename)


if __name__ == "__main__":
    unittest.main()