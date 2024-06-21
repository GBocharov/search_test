import chromadb

from embeddings.api.schema import CollectionName, Collection
from embeddings.infrastructure.chroma_db_config import chroma_db_config
from embeddings.infrastructure.embedding_functions import local_embedding_function

chroma_client = chromadb.HttpClient(host=chroma_db_config.HOST, port=chroma_db_config.PORT)

local_all_12_mini_collection_full = chroma_client.get_or_create_collection(name='all_12_mini_full_text_collection',
                                                                           embedding_function=local_embedding_function)

local_all_12_mini_collection_solutions = chroma_client.get_or_create_collection(name='all_12_mini_solutions_collection',
                                                                                embedding_function=local_embedding_function)


def get_collection(model_name: Collection):
    if model_name.name == 'local_all_12':
        return local_all_12_mini_collection_solutions
    elif model_name.name == 'local_all_12_full':
        return local_all_12_mini_collection_full
    else:
        return None
