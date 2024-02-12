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

""" Just a script to try hitting local LLM endpoints
"""
from openai import OpenAI

class RunLocalQuey:
    def __init__(self):
        self.URLS = ["http://localhost:8000/v1",]

    def get_response(self,prompt):
        for url in self.URLS:
            print(f"{url:*^50}")
            client = OpenAI(api_key="foo",base_url=url,)
            chat_completion = client.chat.completions.create(
                messages=[
                    { 
                        "role": "user",
                        "content": f"{prompt}",
                    },
                ],
                model="",
            )
            
            for choice in chat_completion.choices:
                return choice.message.content

