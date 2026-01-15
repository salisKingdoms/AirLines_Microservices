import asyncpg
from datetime import datetime

class AirlineRepository:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def search_airlines(self, name: str| None, code: str | None, is_active: bool | None, page: int=1, page_size: int = 10):
        query="""
            SELECT id, name, code, logo_url, country, founded_year, is_active
                FROM airlines
            WHERE 1=1
            """
        
        params = []
        idx=1

        if name:
            query += f" AND name ILIKE ${idx}"
            params.append(f"%{name}%")
            idx +=1

        if code:
            query += f" AND code ILIKE ${idx}"
            params.append(f"%{code}%")
            idx +=1

        if is_active is not None:
            query += f" AND is_active = ${idx}"
            params.append(is_active)
            idx +=1

        query +=" ORDER BY name, country"

        offset = (page - 1)* page_size
        query += f" LIMIT ${idx} OFFSET ${idx + 1}"
        params.extend([page_size, offset])

        return await self.conn.fetch(query, *params)