from typing import List, Callable
from dataclasses import dataclass
from enum import Enum
import logging
import textwrap


# Internal function, don't call this directly
def _run_prompt(prompt: str, completion: Callable[[str], any]) -> dict:
    response = {}
    try:
        logging.debug(prompt)
        response = completion(prompt) # return type: json object as a dict
        logging.debug(response)
    except Exception as e:
        logging.error(e)
    return response            



class SortOrder(Enum):
    ascending = 1
    descending = -1
    
@dataclass
class SortPrompt:
    system_role: str
    items: List[str]
    order: SortOrder
    criterion: str

    def to_str(self) -> str:
        items = ", ".join(self.items)
        prompt = """
            ### Instructions
            You are {system_role}.
            Your task is to sort below list of items in {order} order according to {criterion}.
            Once you have sorted them, provide a reasoning for the sort order you have selected.
            Return the output as a JSON object in the format:
            {{
                "result": ["item 1", "item 2", ..., "item n"],
                "sort_order": "EITHER ascending OR descending",
                "sort_criterion": "the criterion applied to sort",
                "reason": "description why you sorted all items accordigly"
            }}
            ### Example
            List of items to sort: ["house", "racing horse", "bicyle", "pizza"]
            Sort order: ascending
            Sort criterion: purchasing price
            Expected output:
            {{
                "result": ["pizza", "bicycle", "racing horse", "house"],
                "reason": "A house is more expensive than a racing horse. A racing horse is more expensive than a bicycle. A bicycle is more expensive than a pizza.",
                "sort_order": "ascending",
                "sort_criterion": "purchasing price"
            }}
            ### Input
            {items}""".format(system_role=self.system_role, order=self.order.name, criterion=self.criterion, items=items)  
        return textwrap.dedent(prompt).strip()

def sort(prompt: str, completion: Callable[[str], any]) -> dict:
    """Sorts a list of concepts (strings) according to a given criterion

    Parameters
    ----------
    prompt : str
        A prompt string assembled from SortPrompt. Defines:
        1. a list of concepts to be sorted,
        2. a sort order (either ascending or descending)
        3. a sort criterion.

    completion : Callable[[str], any]
        A completion function that accepts a prompt as a string and returns a json object

    Returns
    -------
    dict
        A json object as the output of the language model.
        The dict must contain at least two key-value pairs:
        1. "result": [...the list of sorted concepts...]
        2. "reason": "...the reasoning provided for the sorting decisions..."
        3. (Optional) Further key-value pairs such as the sort order or the sort criterion
    """
    logging.debug("pygape.sort: Sending prompt to completion API")
    response = _run_prompt(prompt, completion) # return type: json object as a dict
    return response



@dataclass
class FilterPrompt:
    system_role: str
    items: List[str]
    criterion: str

    def to_str(self) -> str:
        items = ", ".join(self.items)
        prompt = """
            ### Instructions
            You are {system_role}.
            Your task is to filter below list of items according to {criterion}.
            Also provide a reason for each item that you kept why you did not filter it out.
            Return the output as a JSON object in the format:
            {{
                "result": ["item 1", "item 2", ..., "item n"],
                "reason": ["reason to keep item 1", "reason to keep item 2", ..., "reason to keep item n"],
                "filter_criterion": "the criterion applied to filter"
            }}
            ### Example
            List of items to filter: ["house", "racing horse", "bicyle", "pizza"]
            Filter criterion: a person can ride this object
            Expected output:
            {{
                "result": ["pizza", "bicycle", "racing horse", "house"],
                "reason": ["a person cannot ride a pizza", "a person can ride a bidycle", "a person can ride a racing horse", "a person cannot ride a house"],
                "filter_criterion": "" 
            }}
            ### Input
            {items}""".format(system_role=self.system_role, criterion=self.criterion, items=items)
        return textwrap.dedent(prompt).strip()

def filter(prompt: str, completion: Callable[[str], any]) -> dict:
    """Filters a list of concepts (strings) according to a given criterion

    Parameters
    ----------
    prompt : str
        A prompt string assembled from FilterPrompt. Defines:
        1. a list of concepts to be filtered,
        2. a filter criterion.

    completion : Callable[[str], any]
        A completion function that accepts a prompt as a string and returns a json object

    Returns
    -------
    dict
        A json object as the output of the language model.
        The dict must contain at least two key-value pairs:
        1. "result": [...the list of filtered concepts...]
        2. "reason": "[...a list of reasons for filter deicions...]"
        3. (Optional) Further key-value pairs such as the filter criterion applied
    """
    logging.debug("pygape.filter: Sending prompt to completion API")
    response = _run_prompt(prompt, completion) # return type: json object as a dict
    return response


@dataclass
class FindPrompt:
    system_role: str
    items: List[str]
    criterion: str
    
    def to_str(self) -> str:
        items = ", ".join(self.items)
        prompt = """
            ### Instructions
            You are {system_role}.
            Your task is to find the first item in the list that matches the criterion: {criterion}.
            Also provide a reason why you picked this item but not any of the other items in the list.
            Return the output as a JSON object in the format:
            {{
                "result": "the first item found in the list that matches the given criterion",
                "reason": "reason why you picked this item and not any others prior to it",
                "matching_criterion": "the matching criterion applied"
            }}
            ### Example
            List of items ["Paris", "Rome", "Canberra", "Singapore", "Albuquerque", "Berlin", "London", "Krakow", "Dar Es Salaam"]
            Criterion: This city is not a capital of its country.
            Expected output:
            {{
                "result": "Albuquerque",
                "reason": "Albuquerque is the first item in the list that is not the capital of its country (USA). Also Krakow is not the capital of Poland, and Dar Es Salaam is not the capital of Tanzania, but they occurr later in the list.",
                "matching_criterion": "is not the capital city of the country it belongs to" 
            }}
            ### Input
            {items}""".format(system_role=self.system_role, criterion=self.criterion, items=items)
        return textwrap.dedent(prompt).strip()   

def find(prompt: str, completion: Callable[[str], any]) -> dict:
    """Finds the first concept (list item) in a list of concept that matches a certain criterion 

    Parameters
    ----------
    prompt : str
        A prompt string assembled from FindPrompt. Defines:
        1. a list of concepts to be searched,
        2. a matching criterion.

    completion : Callable[[str], any]
        A completion function that accepts a prompt as a string and returns a json object

    Returns
    -------
    dict
        A json object as the output of the language model.
        The dict must contain at least two key-value pairs:
        1. "result": "the first concept (item) found matching in the list"
        2. "reason": "the reasoning provided why the item matches"
        3. (Optional) Further key-value pairs such as the matching criterion applied
    """
    logging.debug("pygape.find: Sending prompt to completion API")
    response = _run_prompt(prompt, completion) # return type: json object as a dict
    return response


@dataclass
class ConditionPrompt:
    system_role: str
    statement: str

    def to_str(self) -> str:
        prompt = """
            ### Instructions
            You are {system_role}.
            Your task is to decide if the statement given below is true or false.
            Return the output as a JSON object in the format:
            {{
                "result": "true OR false",
                "reason": "The reason for your decision"
            }}
            ### Example
            Statement: Water freezes at 100 degrees Celsius.
            Expected output:
            {{
                "result": "false",
                "reason": "Water freezes at 0 degree Celsious, but it boils at 100 degrees Celsius."
            }}
            ### Input
            {statement}""".format(system_role=self.system_role, statement=self.statement)
        return textwrap.dedent(prompt).strip()

def condition(prompt: str, completion: Callable[[str], any]) -> dict:
    """Returns either True or False given a certain statement

    Parameters
    ----------
    prompt : str
        A prompt string assembled from ConditionPrompt. Defines:
        1. a statement that can either be true or false

    completion : Callable[[str], any]
        A completion function that accepts a prompt as a string and returns a json object

    Returns
    -------
    dict
        A json object as the output of the language model.
        The dict must contain at least two key-value pairs:
        1. "result": "True" OR "False"
        2. "reason": "the reasoning provided why the statement is true or false"
        3. (Optional) Further key-value pairs
    """
    logging.debug("pygape.condition: Sending prompt to completion API")
    response = _run_prompt(prompt, completion) # return type: json object as a dict
    return response
