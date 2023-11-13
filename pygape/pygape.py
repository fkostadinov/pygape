from typing import List, Callable
from dataclasses import dataclass
from enum import Enum
import textwrap



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
                "sort_order": "ascending",
                "sort_criterion": "purchasing price",
                "reason": "A house is more expensive than a racing horse. A racing horse is more expensive than a bicycle. A bicycle is more expensive than a pizza."
            }}
            ### Input
            {items}""".format(system_role=self.system_role, order=self.order.name, criterion=self.criterion, items=items)  
        return textwrap.dedent(prompt).strip()

def sort(prompt: str, completion: Callable, print_prompt=False) -> str:
    
    if print_prompt:
        print(prompt)
    
    try:
        response = completion(prompt)
            
    #except json.JSONDecodeError as e:
    #    # Handle JSON decode error (e.g., JSON is malformed)
    #    print(f"txt2struct.sort: JSONDecodeError: {e.msg}")
    #except TypeError as e:
    #    # Handle wrong type error (e.g., passing a non-string/non-bytes)
    #    print(f"txt2struct.sort: TypeError: {e}")    
    except Exception as e:
        print(f"txt2struct.sort: Error: {e}")
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

def filter(prompt: str, completion: Callable, print_prompt=False) -> str:
    if print_prompt:
        print(prompt)
    
    try:
        response = completion(prompt)
    except Exception as e:
        print(f"Exception: {e}")
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
            Your task is to find the first item in the list that fulfills the criterion: {criterion}.
            Also provide a reason why you picked this item but not any of the other items in the list.
            Return the output as a JSON object in the format:
            {{
                "result": "the first item found in the list that fulfills the given criterion",
                "reason": "reason why you picked this item and not any others prior to it",
                "filter_criterion": "the criterion applied"
            }}
            ### Example
            List of items ["Paris", "Rome", "Canberra", "Singapore", "Albuquerque", "Berlin", "London", "Krakow", "Dar Es Salaam"]
            Criterion: This city is not a capital of its country.
            Expected output:
            {{
                "result": "Albuquerque",
                "reason": "Albuquerque is the first item in the list that is not the capital of its country (USA). Also Krakow is not the capital of Poland, and Dar Es Salaam is not the capital of Tanzania, but they occurr later in the list.",
                "filter_criterion": "is not the capital city of the country it belongs to" 
            }}
            ### Input
            {items}""".format(system_role=self.system_role, criterion=self.criterion, items=items)
        return textwrap.dedent(prompt).strip()   
    

def find(prompt: str, completion: Callable, print_prompt=False) -> str:
    if print_prompt:
        print(prompt)
    
    try:
        response = completion(prompt)
    except Exception as e:
        print(f"Exception: {e}")
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
    
def condition(prompt: str, completion: Callable, print_prompt=False) -> str:
    if print_prompt:
        print(prompt)
        
    try:
        response = completion(prompt)
    except Exception as e:
        print(f"Exception: {e}")
    return response
            





"""
def sort(concepts_to_sort: List[str]) -> any:
    
    sort_function = [
        {
            "name": "sort",
            "description": "Sorts a list of concepts according to a given criterion and order",
            "parameters": {
                "type": "object",
                "properties": {
                    "concepts_to_sort": {
                        "type": "string",
                        "description": "A comma-separated list of concepts that should be sorted"
                    },
                    "sort_criterion": {
                        "type": "string",
                        "description": "The criterion by which to sort the concepts"
                    },
                    "order": {
                        "type": "string",
                        "enum": ["ascending", "descending"],
                        "description": "The sort order, either ascending or descending",
                    }
                }
            }
        }
    ]
    
    concepts_str = ", ".join(concepts_to_sort)
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [{'role': 'user', 'content': concepts_str}],
        functions = sort_function,
        function_call = 'auto'
    )

    # Loading the response as a JSON object
    json_response = json.loads(response['choices'][0]['message']['function_call']['arguments'])
    print(json_response)
    
    
    return json_response
"""