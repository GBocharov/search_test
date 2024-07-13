from abc import ABC, abstractmethod

from chromadb import QueryResult


class OutputParseFunction(ABC):
    @abstractmethod
    def __call__(self, chroma_outputs: QueryResult):
        pass


class SimpleOutputParser(OutputParseFunction):
    def __call__(self, chroma_outputs: QueryResult):
        pass
