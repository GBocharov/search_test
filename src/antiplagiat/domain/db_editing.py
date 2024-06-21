import pandas as pd
from fastapi import Query
from langchain_text_splitters import split_text_on_tokens

from embeddings.api.schema import SaveDataRequest, SearchRequest, CollectionName, Collection, default_model
from embeddings.domain.chroma_utils import add_vectors_to_db, search
from file_processing.text_splitters.ru_token_splitter import RU_TOKEN_SPLITTER


async def compose_full_text_request(dataframe, encoding_model):
    docs = []
    metadatas = []
    text_spliter = RU_TOKEN_SPLITTER(tokens_per_chunk=500, chunk_overlap=50)
    for index, item in dataframe.iterrows():
        IdGuid = item['IdGuid']
        Name = item['Name']
        Problem = item['Problem']
        Solution = item['Solution']
        Result = item['Result']
        text = f'{Problem} \n {Solution} \n {Result} \n'

        chunks = split_text_on_tokens(text=text, tokenizer=text_spliter)
        docs += chunks
        metadata = [{'IdGuid': IdGuid, 'Name': Name} for _ in chunks]
        metadatas += metadata

    return SaveDataRequest(encoding_model=encoding_model, documents=docs, metadatas=metadatas)


async def compose_solution_text_request(dataframe, encoding_model):
    docs = []
    metadatas = []
    text_spliter = RU_TOKEN_SPLITTER(tokens_per_chunk=500, chunk_overlap=50)
    for index, item in dataframe.iterrows():
        IdGuid = item['IdGuid']
        Name = item['Name']
        Problem = item['Problem']
        Solution = item['Solution']
        Result = item['Result']
        text = f'{Solution} \n'

        chunks = split_text_on_tokens(text=text, tokenizer=text_spliter)
        docs += chunks
        metadata = [{'IdGuid': IdGuid, 'Name': Name} for _ in chunks]
        metadatas += metadata

    return SaveDataRequest(encoding_model=encoding_model, documents=docs, metadatas=metadatas)


async def fill_rag_db(encoding_model: Collection = Query(default_model)):
    df1 = pd.read_csv('/opt/app-root/datasets/ideas.csv')

    if 'full' in encoding_model.name:
        request = await compose_full_text_request(df1, encoding_model)
    else:
        request = await compose_solution_text_request(df1, encoding_model)

    await add_vectors_to_db(request)
