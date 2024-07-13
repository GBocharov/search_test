from typing import Union, List

import chromadb
from chromadb import Documents, EmbeddingFunction
from fastapi import Query

from data_processing.output_parse_functions import OutputParseFunction
from data_processing.parse_inserts_functions import ParseInsertsFunction
from data_processing.parse_request_functions import ParseRequestsFunction
from vector_storage.infrastructure.chroma_db_config import chroma_db_config

BATCH_SIZE = 100
chroma_client = chromadb.HttpClient(host=chroma_db_config.HOST, port=chroma_db_config.PORT)


class Strategy:
    def __init__(self, collection_name: str,
                 embedding_f: EmbeddingFunction[Documents],
                 parse_inserts_f: ParseInsertsFunction,
                 parse_search_requests_f: ParseRequestsFunction,
                 parse_output_f: OutputParseFunction,
                 db_client=chroma_client  # fuck
                 ):
        self.embedding_f = embedding_f
        # check?
        self.collection = db_client.get_or_create_collection(name=collection_name, embedding_function=embedding_f)
        self.parse_inserts_f = parse_inserts_f
        self.parse_search_requests_f = parse_search_requests_f
        self.parse_output_f = parse_output_f

    def add(self, insert_inputs: Union[str, dict, List[str], List[dict]]) -> str:
        # Union[str, dict, List[str], List[dict]] -> OneOrMany
        # Success info?
        # skip bad chunk?
        insert_request = self.parse_inserts_f(insert_inputs)

        for i in range(0, len(insert_request.documents), BATCH_SIZE):
            try:
                docs = insert_request.documents[i: i + BATCH_SIZE]
                metas = insert_request.metadatas[i: i + BATCH_SIZE]
                start = self.collection.count()
                ids = [str(i) for i in range(start, start + len(docs))]
                self.collection.add(ids=ids, documents=docs, metadatas=metas)
            except Exception as e:
                # pass?
                raise Exception(f'Save error! : {e}')

        return f'Vectors successfully saved, v_count = {self.collection.count()}'

    def query(self,
              search_request: Union[str, dict, List[str], List[dict]],
              n_results: int = 10,
              include_embeddings: bool = False
              ):

        search_request = self.parse_search_requests_f(search_request)

        return self.collection.query(query_texts=search_request.documents, n_results=n_results,
                                     include=include_embeddings, where=search_request.where)

    def get(self,
            n_results: int = 10,
            offset: int = 0,
            include_embeddings: bool = False,
            where: dict = None):
        print(type(n_results))
        print(type(offset))
        ids = [str(i) for i in range(offset, n_results + offset)]
        res = self.collection.get(ids=ids,
                                  include=["metadatas", "documents"] + (["embeddings"] if include_embeddings else []),
                                  where=where)
        return res

    def delete(self):
        pass
