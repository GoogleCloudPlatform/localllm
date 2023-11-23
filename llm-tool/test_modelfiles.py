import unittest

import modelfiles


class TestModels(unittest.TestCase):
    def test_filter_models(self):
        files = [
            "openinstruct-mistral-7b.Q4_K_M.gguf",
            "foo.py",
            "bar",
            "some_dir/",
            ".somedotfile",
        ]
        m = modelfiles.filter_models(files)
        self.assertEqual(1, len(m))
        self.assertEqual("openinstruct-mistral-7b.Q4_K_M.gguf", m[0])


if __name__ == "__main__":
    unittest.main()