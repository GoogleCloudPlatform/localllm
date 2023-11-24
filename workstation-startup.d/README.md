# workstation-startup.d

As described in [the cloud workstation docs](https://cloud.google.com/workstations/docs/customize-container-images#home_directory_modifications)
modifications to the home directory should be done in start up scripts.

We need to move the downloaded models from the root user cache to the user
specific cache dir expected by https://github.com/huggingface/huggingface_hub
once the user is created.