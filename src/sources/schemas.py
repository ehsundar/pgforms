from typing import List

from pydantic import BaseModel

from src.sources.models import Source


class ListSourcesResponse(BaseModel):
    sources: List[Source]
