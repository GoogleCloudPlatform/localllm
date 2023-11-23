import unittest

import modelserving


class TestServing(unittest.TestCase):
    procs = [
        ['/bin/bash', '/google/scripts/entrypoint.sh'],
        ['/usr/bin/dockerd', '-p', '/var/run/docker.pid', '--data-root', '/home/.docker_data', '--mtu=1460'],
        ['containerd', '--config', '/var/run/docker/containerd/containerd.toml'],
        ['sh', './bin/codeoss-cloudworkstations', '--port=80', '--host=0.0.0.0'],
        ['/opt/code-oss/node', '/opt/code-oss/out/bootstrap-fork', '--type=ptyHost', '--logsPath', '/home/user/.codeoss-cloudworkstations/data/logs/20231123T170240'],
        ['python3', '-m', 'llama_cpp.server', '--model', '/models/llama-2-13b-ensemble-v5.Q4_K_M.gguf', '--host', '0.0.0.0', '--port', '8000'],
        ['/bin/bash', '--init-file', '/opt/code-oss/out/vs/workbench/contrib/terminal/browser/media/shellIntegration-bash.sh'],
        ['/bin/bash', '--init-file', '/opt/code-oss/out/vs/workbench/contrib/terminal/browser/media/shellIntegration-bash.sh'],
    ]

    def test_is_running_running(self):
        self.assertTrue(modelserving.is_running('llama-2-13b-ensemble-v5.Q4_K_M.gguf', self.procs))

    def test_is_running_not_running(self):
        self.assertFalse(modelserving.is_running('openinstruct-mistral-7b.Q4_K_M.gguf', self.procs))


if __name__ == "__main__":
    unittest.main()