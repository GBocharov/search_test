from typing import List, Union

from pydantic import BaseModel


class StringInsertRequest(BaseModel):
    items: Union[str, List[str]]

    class Config:
        json_schema_extra = {
            "examples":
                [
                    {
                        "items": ["string1",
                                  "string2",
                                  "string3"]
                    }
                ]
        }


class IdsInsertRequest(BaseModel):
    items: Union[str, List[str]]

    class Config:
        json_schema_extra = {
            "examples":
                [
                    {
                        "items": ["id1",
                                  "id2",
                                  "id2"]
                    }
                ]
        }
