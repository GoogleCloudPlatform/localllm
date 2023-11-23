# localllm

Run LLMs locally on Cloud Workstations. Uses:

* Quantized models from HuggingFace
* [llama-cpp-python's webserver](https://github.com/abetlen/llama-cpp-python#web-server)

## Getting started so far

```bash
python3 -m venv ~/.localllm
source ~/.localllm/bin/activate
pip3 install -r requirements.txt

wget https://huggingface.co/TheBloke/Llama-2-13B-Ensemble-v5-GGUF/resolve/main/llama-2-13b-ensemble-v5.Q4_K_M.gguf
wget https://huggingface.co/TheBloke/openinstruct-mistral-7B-GGUF/resolve/main/openinstruct-mistral-7b.Q4_K_M.gguf

python3 -m llama_cpp.server --model llama-2-13b-ensemble-v5.Q4_K_M.gguf --host 0.0.0.0 --port 8000
python3 -m llama_cpp.server --model openinstruct-mistral-7b.Q4_K_M.gguf --host 0.0.0.0 --port 8001
```

Try it out with the script (from the virtual env ^^):

```bash
(.localllm) ./trylocal.py
```