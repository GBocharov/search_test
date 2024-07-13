from typing import List, Union

from fastapi import APIRouter

from antiplagiat.domain.strategy import strategy

antiplagiat_router = APIRouter(
    prefix="/antiplagiat_router",
    tags=["antiplagiat"],
)


@antiplagiat_router.post(
    "/insert_into_db",
)
async def fill_db(inputs: Union[str, List[str]]):
    strategy.add(inputs)
    return strategy.get(n_results=1)


@antiplagiat_router.post(
    "/get_top_db",
)
async def get_top_db(
            n_results: int = 10,
            offset: int = 0,
            include_embeddings: bool = False):
    strategy.get(n_results, offset, include_embeddings)
    return

