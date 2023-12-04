import logging
import json
from openai import OpenAI

def openai_completion(prompt: str) -> any:
    response = (None, None, None)
    try:
        client = OpenAI()
        completion = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages = [
                {"role": "user", "content": prompt},
            ],
            temperature=0.00000001)

        # Async
        #from openai import AsyncOpenAI
        #client = AsyncOpenAI()
        #completion = await client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])

        # Extract the json string response from the OpenAIObject
        json_str = completion.choices[0].message.content

        # Creaate a json object of type dict. According to prompt conventions, each json objct
        # should at least have a key "result" and "reason" plus optionally other keys
        response = json.loads(json_str)

    except Exception as e:
        logging.error(e)

    return response