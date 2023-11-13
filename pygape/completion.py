import openai

def openai_completion(prompt: str) -> any:
    try:
        openai_response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-1106",
            messages = [
                {"role": "user", "content": prompt},
            ],
            # Note: If we set the temperature to 0.0 then the results are not always consistent.
            # Let's try to set it instead to an extremely small value above 0.
            # See here: https://community.openai.com/t/why-the-api-output-is-inconsistent-even-after-the-temperature-is-set-to-0/329541/9
            temperature = 0.00000001
        )
    except Exception as e:
        print(f"completion.openai_completion: Exception: {e}")
        
    return openai_response