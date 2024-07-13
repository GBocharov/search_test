import datetime
from typing import Union, List
from abc import ABC, abstractmethod

from langchain_text_splitters import Tokenizer, split_text_on_tokens

from data_processing.schema import SearchRequest


class ParseRequestsFunction(ABC):
    '''Base'''

    @abstractmethod
    def __call__(self, insert_input: Union[List[str], List[dict]]) -> SearchRequest:
        pass


class SimpleIdeasRequestsParser(ParseRequestsFunction):
    '''For IdeasTable'''

    def __init__(self, text_splitter: Tokenizer):
        self.text_splitter = text_splitter

    def _parse_dicts(self, inputs: List[dict]):
        docs = []
        for item in inputs:
            IdGuid = item['IdGuid']
            Name = item['Name']
            Problem = item['Problem']
            Solution = item['Solution']
            Result = item['Result']

            Date = item['DateCreated'].split('.')[0]
            Date = datetime.datetime.strptime(Date, "%Y-%m-%d %H:%M:%S")
            Date = int(Date.timestamp())

            text = f'{Name} \n {Problem} \n {Solution} \n {Result} \n'

            chunks = split_text_on_tokens(text=text, tokenizer=self.text_splitter)
            docs += chunks

        return SearchRequest(documents=docs)

    def _parse_strs(self, inputs: List[str]):
        docs = inputs.copy()

        return SearchRequest(documents=docs)

    def __call__(self, insert_input: Union[str, dict, List[str], List[dict]]) -> SearchRequest:
        if isinstance(insert_input, str) or isinstance(insert_input, dict) or not hasattr(insert_input, '__len__'):
            insert_input = [insert_input]

        if all(isinstance(item, str) for item in insert_input):
            return self._parse_strs(insert_input)
        elif all(isinstance(item, str) for item in insert_input):
            return self._parse_dicts(insert_input)
        else:
            raise Exception("Value mast be Union[str, dict, List[str], List[dict]]")
