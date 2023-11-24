from setuptools import setup

setup(
    name='llm',
    version='0.0.1',
    py_modules=[
        'llm',
        'modeldownload',
        'modelfiles',
        'modelserving',
    ],
    install_requires=[
        'Click',
        'llama-cpp-python[server]',
        'psutil',
        'huggingface_hub'
    ],
    entry_points={
        'console_scripts': [
            'llm = llm:cli',
        ],
    },
)