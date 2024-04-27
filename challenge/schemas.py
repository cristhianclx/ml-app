from typing import List, Literal

from pydantic import BaseModel

from .constants import AIRLINES


class Flight(BaseModel):
    OPERA: Literal[tuple(AIRLINES)]
    TIPOVUELO: Literal["I", "N"]
    MES: Literal[tuple([m for m in range(1, 13)])]


class PredictData(BaseModel):
    flights: List[Flight]
