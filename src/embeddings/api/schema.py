from enum import Enum
from typing import List, Dict

from fastapi import Query
from pydantic import BaseModel


default_model = 'local_all_12_full'


class Collection(str, Enum):
    gigachat = 'gigachat'
    local_all_12 = 'local_all_12'
    local_all_12_full = 'local_all_12_full'
    openai = 'openai'


class EmbeddingRequest(BaseModel):
    id: str
    text: str


class SearchRequest(BaseModel):
    text: str


class CollectionName(BaseModel):
    model: Collection = Query(default_model)


class SaveDataRequest(BaseModel):
    encoding_model: Collection = Query(default_model)
    documents: List[str]
    metadatas: List[Dict]
