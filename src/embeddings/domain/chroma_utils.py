import logging
from typing import List
from fastapi import Query
from embeddings.domain.collections import get_collection
from embeddings.api.schema import SaveDataRequest, SearchRequest, CollectionName, Collection, default_model

BATCH_SIZE = 100


async def add_vectors_to_db(request: SaveDataRequest):
    collection = get_collection(request.encoding_model)
    print(f'-------------------->{collection.name}')
    for i in range(0, len(request.documents), BATCH_SIZE):
        try:
            documents = request.documents[i: i + BATCH_SIZE]
            metadatas = request.metadatas[i: i + BATCH_SIZE]
            start = collection.count()
            ids = [str(i) for i in range(start, start + len(documents))]
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
        except Exception as e:
            return 'save error!'
    return f'vector count = {collection.count()}'


async def search(
        request: SearchRequest,
        encoding_model: Collection = Query(default_model),
        n_results: int = Query(10),
        include_embeddings: bool = Query(False),
        ids: List[str] = Query([], alias="id"),
):
    collection = get_collection(encoding_model)

    where = {'id': {'$nin': ids}} if ids else None
    include = ["metadatas", "documents", "distances"] + (["embeddings"] if include_embeddings else [])

    return collection.query(
        query_texts=request.text,
        n_results=n_results,
        include=include,
        where=where
    )


async def top_chunks(
        encoding_model: Collection = Query(default_model),
        n_results: int = Query(10),
        offset: int = Query(0),
        include_embeddings: bool = Query(False)):

    collection = get_collection(encoding_model)
    ids = [str(i) for i in range(offset, n_results + offset)]
    res = collection.get(ids=ids,
                         include=["metadatas", "documents"] + (["embeddings"] if include_embeddings else []))
    return res
