import datetime
from typing import Union, List
from abc import ABC, abstractmethod

from chromadb.api.types import OneOrMany
from langchain_text_splitters import Tokenizer, split_text_on_tokens

from data_processing.schema import InsertDataRequest


class ParseInsertsFunction(ABC):
    '''Base'''

    @abstractmethod
    def __call__(self, insert_input:  Union[OneOrMany[str], OneOrMany[dict]]) -> InsertDataRequest:
        pass


class SimpleIdeasInsertParser(ParseInsertsFunction):
    '''For IdeasTable'''

    def __init__(self, text_splitter: Tokenizer):
        self.text_splitter = text_splitter

    def _parse_dicts(self, inputs: List[dict]):
        docs = []
        metadatas = []
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
            metadata = [{'IdGuid': IdGuid, 'Name': Name, 'Date': Date} for _ in chunks]
            metadatas += metadata

        return InsertDataRequest(documents=docs, metadatas=metadatas)

    def _parse_strs(self, inputs: List[str]):
        docs = inputs.copy()
        metadatas = [{'IdGuid': '0', 'Name': '0', 'Date': 0} for _ in range(len(inputs))]

        return InsertDataRequest(documents=docs, metadatas=metadatas)

    def __call__(self, insert_input: Union[OneOrMany[str], OneOrMany[dict]]) -> InsertDataRequest :
        if isinstance(insert_input, str) or isinstance(insert_input, dict) or not hasattr(insert_input, '__len__'):
            insert_input = [insert_input]

        if all(isinstance(item, str) for item in insert_input):
            return self._parse_strs(insert_input)
        elif all(isinstance(item, str) for item in insert_input):
            return self._parse_dicts(insert_input)
        else:
            raise Exception("Value mast be Union[str, dict, List[str], List[dict]]")

