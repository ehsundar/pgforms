import re
from typing import Annotated, List

import asyncpg
import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import conint
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from starlette import status

from src.database import get_db
from src.dependencies import get_current_user
from src.sources import guest_queries
from src.sources.queries import AsyncQuerier
from src.sources.schemas import ListSourcesResponse, ListTablesResponse, TableColumn, TableColumnsResponse, \
    TableRowsResponse
from src.users.models import User

router = APIRouter(prefix="/sources", tags=["sources"])

postgres_driver_replacement_regex = re.compile(r"(?P<schema>postgresql)://(?P<connection>.+)")


@router.get("/", response_model=ListSourcesResponse)
async def list_sources(
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
):
    conn = await db.connection()

    queirer = AsyncQuerier(conn)

    sources = []
    async for s in queirer.list_sources(owner=current_user.username):
        sources.append(s)

    return ListSourcesResponse(sources=sources)


@router.get("/introspection/{source_id}", response_model=ListTablesResponse)
async def get_tables(
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
        source_id: int,
):
    conn = await db.connection()
    querier = AsyncQuerier(conn)
    source = await querier.get_source(id=source_id)
    if not source:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if source.owner != current_user.username:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    conn_string = postgres_driver_replacement_regex.sub(r"\g<schema>+asyncpg://\g<connection>", source.conn_string)
    engine = create_async_engine(conn_string, echo=True)
    async_session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

    async with async_session() as guest_db:
        guest_conn = await guest_db.connection()
        guest_querier = guest_queries.AsyncQuerier(guest_conn)

        tables = []
        async for t in guest_querier.list_tables():
            tables.append(t)

        return ListTablesResponse(tables=tables)


@router.get("/introspection/{source_id}/tables/{table_name}/columns", response_model=TableColumnsResponse)
async def get_table_columns(
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
        source_id: int,
        table_name: str,
        table_schema: str = "public",
):
    conn = await db.connection()
    querier = AsyncQuerier(conn)
    source = await querier.get_source(id=source_id)
    if not source:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if source.owner != current_user.username:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    conn_string = postgres_driver_replacement_regex.sub(r"\g<schema>+asyncpg://\g<connection>", source.conn_string)
    engine = create_async_engine(conn_string, echo=True)
    async_session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

    async with async_session() as guest_db:
        guest_conn = await guest_db.connection()
        guest_querier = guest_queries.AsyncQuerier(guest_conn)

        columns = []
        async for c in guest_querier.list_table_columns(table_schema=table_schema, table_name=table_name):
            columns.append(TableColumn.from_query_model(c))

        return TableColumnsResponse(columns=columns)


@router.get("/introspection/{source_id}/tables/{table_name}", response_model=TableRowsResponse)
async def table_rows(
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
        source_id: int,
        table_name: str,
        fields: Annotated[str, Query()],
        table_schema: str = "public",
        limit: int = 30,
):
    if not 0 < limit < 501:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "limit out of range")
    fields_sep = fields.split(",")
    # TODO: Validate each field name

    conn = await db.connection()
    querier = AsyncQuerier(conn)
    source = await querier.get_source(id=source_id)
    if not source:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if source.owner != current_user.username:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    conn_string = postgres_driver_replacement_regex.sub(r"\g<schema>+asyncpg://\g<connection>", source.conn_string)
    engine = create_async_engine(conn_string, echo=True)
    async_session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

    async with async_session() as guest_db:
        guest_conn = await guest_db.connection()

        rows_response = await guest_conn.execute(
            # can not use table name as input parameter, we format query
            # TODO: check schema and table access permission to avoid sql injection
            sqlalchemy.text(f"select {fields} from {table_schema}.{table_name} limit :limit"),
            parameters={"limit": limit},
        )

        rows = []
        for r in rows_response:
            row = {}
            for i, item in enumerate(r):
                row[fields_sep[i]] = item
            rows.append(row)

        return TableRowsResponse(rows=rows)
