import asyncio
from typing import List

from fastapi import Query
from langchain_text_splitters import split_text_on_tokens
from embeddings.api.schema import SaveDataRequest, SearchRequest, CollectionName, default_model, Collection
from embeddings.domain.chroma_utils import add_vectors_to_db, search
from file_processing.text_splitters.ru_token_splitter import RU_TOKEN_SPLITTER
import pandas as pd


all_ideas = pd.read_csv('/opt/app-root/datasets/ideas.csv')

plag_ideas = pd.read_csv('/opt/app-root/datasets/identical_ideas.csv')

async def db_response(request: SearchRequest,
                      encoding_model: Collection = Query(default_model),
                      n_results: int = Query(10),
                      include_embeddings: bool = Query(False),
                      ids: List[str] = Query([], alias="id"), ):
    results = await search(request, encoding_model, n_results, include_embeddings, ids)
    return results


async def calculate_match_count(encoding_model: Collection = Query(default_model)):
    size = len(plag_ideas)
    match = 0
    middle_distance = 0

    for index, item in plag_ideas.iterrows():
        id_ = item['plagId']
        Problem = item['plagProblem']
        Solution = item['plagSolution']
        Result = item['plagResult']
        target_id = item['origId']
        text = f'{Problem} \n {Solution} \n {Result}'

        request = SearchRequest(text=text)
        result = await search(request=request, encoding_model=encoding_model, n_results=5, include_embeddings=False, ids=[id_])

        for n, meta in enumerate(result['metadatas'][0]):
            if target_id == meta['IdGuid']:
                match += 1
                middle_distance+=result['distances'][0][n]
                print(result['distances'][0][n], '---n ', n)
                break


    return f"total_size = {size}, match_count = {match}, percent = {match / size * 100}%, middle_distance = {middle_distance/match}"


async def calculate_le_distance_count(encoding_model: Collection = Query(default_model)):
    df = pd.read_csv('/opt/app-root/datasets/identical_ideas.csv')
    size = len(df)
    match = 0

    for index, item in df.iterrows():
        id = item['plagId']
        Problem = item['plagProblem']
        Solution = item['plagSolution']
        Result = item['plagResult']
        target_id = item['origId']
        text = f'{Problem} \n {Solution} \n {Result}'
        request = SearchRequest(text=text)
        result = await search(request=request, encoding_model=encoding_model, n_results=5, include_embeddings=False)

        if result['distances'][0][0] <= 2.186324268579483:
            match += 1

    return f"total_size = {size}, match_distance_count = {match}"


async def check_item_by_id(id_guid: str, encoding_model: Collection = Query(default_model)):
    df = pd.read_csv('/opt/app-root/datasets/identical_ideas.csv')

    rows = df[df['plagId'] == id_guid]
    if rows.empty:
        return 'ID not found'

    rows = rows.iloc[0]
    Problem = rows['plagProblem']
    Solution = rows['plagSolution']
    Result = rows['plagResult']
    text = f'{Problem} \n {Solution} \n {Result}'
    request = SearchRequest(text=text)
    result = await search(request=request, encoding_model=encoding_model, n_results=10, include_embeddings=False)
    nearest = result['documents'][0][0]
    nearest_score = result['distances'][0][0]

    report = f"Текст Заявления: {text} \n  Наиболее близкий текст: {nearest} \n Мера близости: {nearest_score}".split('\n')

    return report

#if __name__ == '__main__':
     #loop = asyncio.get_event_loop()
    #task1 = loop.create_task(
    #    compose_SaveDatasetRequest_from_csv(r'C:\Users\Gleb\PycharmProjects\patent-rag\src\datasets\data.csv', ''))
    #loop.run_until_complete(asyncio.wait([task1]))
#