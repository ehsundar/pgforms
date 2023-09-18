from typing import List, Optional

from pydantic import BaseModel

from src.sources.guest_queries import ListTablesRow, ListTableColumnsRow
from src.sources.models import Source


class ListSourcesResponse(BaseModel):
    sources: List[Source]


class ListTablesResponse(BaseModel):
    tables: List[ListTablesRow]


class TableColumn(BaseModel):
    name: str
    type: str
    default: Optional[str]
    is_nullable: bool

    @classmethod
    def from_query_model(cls, m: ListTableColumnsRow):
        return cls(
            name=m.column_name,
            type=m.data_type,
            default=m.column_default,
            is_nullable=True if m.is_nullable == "YES" else False,

        )


class TableColumnsResponse(BaseModel):
    columns: List[TableColumn]
