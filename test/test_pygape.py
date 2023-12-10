###
# How to start: python -m unittest test.test_pygape.PyGapeTestCase -v
###

import unittest
import logging
import os
from dotenv import load_dotenv
import openai
import json
from pygape.completion import openai_completion
from pygape.pygape import \
    sort, SortPrompt, SortOrder, \
    filter, FilterPrompt, \
    find, FindPrompt, \
    truthy, TruthyPrompt, \
    condition, ConditionPrompt



class PyGapeTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # TODO: Put this in a config file
        logging.basicConfig(filename='test_out.log', encoding='utf-8', level=logging.DEBUG)

        # Add parent path and .env file in root directory to the test case paths
        dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        load_dotenv(dotenv_path=dotenv_path)
        openai.api_key = os.getenv("OPENAI_API_KEY")  
        super().setUpClass()
    


    def test_sort(self):
        logging.info("################################ test_sort ################################ ")
        sort_params = SortPrompt(
            system_role = "a helpful assistant",
            items = ["cat", "rat", "mouse", "elephant", "fly", "tiger", "bacteria", "goldfish"],
            order = SortOrder.descending,
            criterion = "their physical weight"
        )
        
        expected = ["elephant", "tiger", "cat", "rat", "mouse", "goldfish", "fly", "bacteria"]
        prompt = sort_params.to_str()
        json_response = sort(prompt, openai_completion)
        retrieved = json_response["result"] # type: list
        
        self.assertEqual(len(retrieved), len(expected))
        for i in range(len(expected)):
            self.assertEqual(retrieved[i], expected[i])
    


    def test_filter(self):
        logging.info("################################ test_filter ################################ ")
        filter_params = FilterPrompt(
            system_role = "a helpful assistant",
            items = ["cat", "rock", "house", "elephant", "airplane", "tiger", "bottle", "gold"],
            criterion = "whether they are inanimate. Only keep the animate ones"
        )
        
        expected = ["cat", "elephant", "tiger"]
        prompt = filter_params.to_str()
        json_response = filter(prompt, openai_completion)
        filtered_items = [item.lower() for item in json_response["result"]] # Ensure all strings are lower case; type: list
        reasons_to_keep = json_response["reason"] # type: list
        
        self.assertEqual(len(filtered_items), len(expected))
        for i in range(len(expected)):
            self.assertTrue(expected[i].lower() in filtered_items) # Make sure all strings are lower case


    def test_find(self):
        logging.info("################################ test_find ################################ ")
        find_params = FindPrompt(
            system_role = "a helpful assistant",
            items = ["Lise Meitner", "Marie Curie", "Chien-Shiung Wu", "Alice Augusta Ball", "Marilyn Monroe", "Katherine Johnson"],
            criterion = "this person is or was not a female scientist. In case there exist multiple people with the same name, count them as a female scientist"
        )
        
        expected = "Marilyn Monroe"
        prompt = find_params.to_str()
        json_response = find(prompt, openai_completion)
        found_item = json_response["result"] # Ensure all strings are lower case; type: list
        reason = json_response["reason"] # type: list
        
        self.assertEqual(found_item, expected)


    def test_truthy(self):
        logging.info("################################ test_truthy ################################ ")
        truthy_params = TruthyPrompt(
            system_role = "a fact checking assistant",
            statement = "Planet earth is the largest planet in the solar system."
        )
        
        prompt = truthy_params.to_str()
        json_response = truthy(prompt, openai_completion)
        bool_str = json_response["result"] # type: str
        if bool_str.lower() == "true":
            response = True
        elif bool_str.lower() == "false":
            response = False
        else:
            self.fail(f"Failed to convert result from LM service to a boolean: {bool_str}")
        
        self.assertFalse(response) # Above statement should be recognized as False   


    def test_condition(self):
        logging.info("################################ test_condition ################################ ")
        condition_params = ConditionPrompt(
            system_role = "a fact checking assistant",
            statement = "Green elephants' favorite food is cotton candy.",
            criterion = "The given statement must talk of fantasy animals."
        )
        
        prompt = condition_params.to_str()
        json_response = condition(prompt, openai_completion)
        bool_str = json_response["result"] # type: str
        if bool_str.lower() == "true":
            response = True
        elif bool_str.lower() == "false":
            response = False
        else:
            self.fail(f"Failed to convert result from LM service to a boolean: {bool_str}")
        
        self.assertFalse(response) # Above statement should be recognized as False

        
        
if __name__ == '__main__':
    unittest.main()