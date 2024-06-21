from typing import List

from fastapi import APIRouter, Query

from antiplagiat.domain.db_editing import fill_rag_db
from antiplagiat.domain.utils import db_response, check_item_by_id, calculate_match_count, \
    calculate_le_distance_count
from embeddings.api.schema import SearchRequest, CollectionName, Collection, default_model

antiplagiat_router = APIRouter(
    prefix="/antiplagiat_router",
    tags=["antiplagiat"],
)


@antiplagiat_router.post(
    "/fill_db",
)
async def fill_db(encoding_model: Collection = Query(default_model)):
    res = await fill_rag_db(encoding_model)
    return res


@antiplagiat_router.post(
    "/rag_db_response",
)
async def get_rag_db_response(
        request: SearchRequest,
        encoding_model: Collection = Query(default_model),
        n_results: int = Query(10),
        include_embeddings: bool = Query(False),
        ids: List[str] = Query([], alias="id"),
):
    res = await db_response(request, encoding_model, n_results, include_embeddings, ids)
    return res


@antiplagiat_router.post(
    "/check_by_id",
)
async def get_check_item_by_id(
        id_guid: str,
        encoding_model: Collection = Query(default_model)
):
    res = await check_item_by_id(id_guid, encoding_model)
    return res

@antiplagiat_router.post(
    "/get_metric",
)
async def get_metric(
        encoding_model:Collection = Query(default_model)):
    res = await calculate_match_count(encoding_model)
    return res

@antiplagiat_router.post(
    "/get_distance_metric",
)
async def get_distance_metric(
        encoding_model: Collection = Query(default_model)
):
    res = await calculate_le_distance_count(encoding_model)
    return res


