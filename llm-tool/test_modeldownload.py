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