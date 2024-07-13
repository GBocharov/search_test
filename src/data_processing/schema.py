
from typing import List, Dict, Union, Optional

#from chromadb.types import Where
from pydantic import BaseModel



class InsertDataRequest(BaseModel):
    documents: List[str]
    metadatas: List[dict]


class SearchRequest(BaseModel):
    documents: Union[str, List[str]]
    where: Optional[dict]
    #where: Optional[Where]  ???
