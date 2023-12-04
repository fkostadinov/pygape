## What is Pygape?
_Pygape_ is a Python library that implements some of the fundamental ideas of __Generative AI-Augmented Program Execution (GAPE)__.

## What is Generative AI-Augmented Program Execution (GAPE)?
_GAPE_ is a programming paradigm that mixes formally well-defined program execution with "common sense reasoning" that Generative AI is capable of. This is best illustrated with an example. Imagine a person makes a statement: "Planet earth is a flat disk residing upon the back of a giant turtle." This statement can be either _true_ or _false_ from a scientific perspective. But which one is it? Applying some "common sense reasoning" (we won't go into discussions here what exactly this means) we conclude that the statement is actually _false_.

Until the advent of Generative AI applying "common sense reasoning" to real world problems was largely restricted to the intelligence of human beings. No longer! Today, we can leave the common sense reasoning to a Large Language Model. Consider this:

```python
statement = "Planet earth is a flat disk residing upon the back of a giant turtle."
# Now send the statement to an LLM, apply some common sense reasoning, and return either True or False
is_true = apply_common_sense_reasoning_with_an_llm(statement)
if is_true:
    print("Welcome to the Flat Earth Society!")
else:
    print("Welcome to the scientific community!")
```
Notice how we are hiding the entire complexity of calling the Generative AI and reasoning behind a single function call. Actually, it could equally be a human being who provides the input rather than an LLM. In fact, we might not even care too much who provides the answer, as long as we do receive an answer that we consider trustworthy enough to continue our program execution.

This approach can be used in many ways. Imagine having a list of concepts (represented simply as strings) that you want to filter by some criterion. For example a list of animal names, and you want to remove all animals that are not herbivores. And that's just the start. Besides filtering we could also be sorting a list according to some criterion. We could try to find an element in a list by some criterion. We could invent new meanings for map and reduce functions. And so on, there are too many possibilities to list them all.

Welcome to the world of __Generative AI-Augmented Program Execution__.

For more info, visit [http://fabian-kostadinov.github.io/2023/11/09/genai-augmented-program-execution/].