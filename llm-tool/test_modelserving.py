import unittest

import modelserving


class TestServing(unittest.TestCase):
    procs = [
        (["/bin/bash", "/google/scripts/entrypoint.sh"], 5),
        (["/usr/bin/dockerd", "-p", "/var/run/docker.pid", "--data-root", "/home/.docker_data", "--mtu=1460"], 4534),
        (["containerd", "--config", "/var/run/docker/containerd/containerd.toml"], 4321),
        (["sh", "./bin/codeoss-cloudworkstations", "--port=80", "--host=0.0.0.0"], 8999),
        (["/opt/code-oss/node", "/opt/code-oss/out/bootstrap-fork", "--type=ptyHost", "--logsPath", "/home/user/.codeoss-cloudworkstations/data/logs/20231123T170240"], 567),
        (["python3", "-m", "llama_cpp.server", "--model",
            "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/llama-2-13b-ensemble-v5.Q4_K_M.gguf",
            "--host", "0.0.0.0", "--port", "8000"], 899),
        (["/bin/bash", "--init-file", "/opt/code-oss/out/vs/workbench/contrib/terminal/browser/media/shellIntegration-bash.sh"], 9000),
        (["/bin/bash", "--init-file", "/opt/code-oss/out/vs/workbench/contrib/terminal/browser/media/shellIntegration-bash.sh"], 5666),
    ]

    def test_filter_running_models(self):
        models = modelserving.filter_running_models(self.procs)
        self.assertEqual(1, len(models))
        self.assertEqual("TheBloke/Llama-2-13B-Ensemble-v5-GGUF", models[0][0])
        self.assertEqual("llama-2-13b-ensemble-v5.Q4_K_M.gguf", models[0][1])


if __name__ == "__main__":
    unittest.main()