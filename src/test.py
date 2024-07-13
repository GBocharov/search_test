from typing import Union, List

from fastapi import Query


def f(a  = Query(default=0, le=5, ge=4444)):
    print(a)
    print(type(a))

f()
f(155)
