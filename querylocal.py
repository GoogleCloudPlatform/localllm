#!/usr/bin/env python3
""" Just a script to try hitting local LLM endpoints
"""

from openai import OpenAI
URLS = [
    "http://localhost:8000/v1",
]
for url in URLS:
    print(f"{url:*^50}")
    client = OpenAI(
        api_key="foo",
                 base_url=url,
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Please write a haiku about cats",
            },
        ],
        model="",
    )
    for choice in chat_completion.choices:
        print(choice.message.content)