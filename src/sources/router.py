import re
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from starlette import status

from src.database import get_db
from src.dependencies import get_current_user
from src.sources import guest_queries
from src.sources.queries import AsyncQuerier
from src.sources.schemas import ListSourcesResponse, ListTablesResponse
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
