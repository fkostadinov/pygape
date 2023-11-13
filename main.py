import os
from dotenv import load_dotenv
import json
import openai
from pygape.pygape import sort, SortPrompt, SortOrder
from pygape.completion import openai_completion


def main():    
    sort_params = SortPrompt(
        system_role = "a helpful assistant",
        items = ["cat", "rat", "mouse", "elephant", "fly", "tiger", "bacteria", "goldfish"],
        order = SortOrder.descending,
        criterion = "their physical weight"
    )
    prompt = sort_params.to_str()
    response = sort(prompt, openai_completion)
    
    print(type(response))
    print(response['choices'][0]['message']['content'])
    print()



if __name__ == "__main__":
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    main()