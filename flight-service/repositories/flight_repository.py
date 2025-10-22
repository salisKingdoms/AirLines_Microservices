import asyncpg
from datetime import datetime, timedelta

class FlightRepository:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def search_flights(self, departure_airport: str, arrival_airport: str, departure_date: str):
        # Find airport IDs
        dep_airport = await self.conn.fetchrow(
            "SELECT id FROM airports WHERE code = $1 AND is_active = TRUE", departure_airport
        )
        arr_airport = await self.conn.fetchrow(
            "SELECT id FROM airports WHERE code = $1 AND is_active = TRUE", arrival_airport
        )
        if not dep_airport or not arr_airport:
            return []

        date_obj = datetime.strptime(departure_date, "%Y-%m-%d")
        next_day = date_obj + timedelta(days=1)

        rows = await self.conn.fetch(
            """
            SELECT 
                f.id, f.flight_number, f.departure_time, f.arrival_time,
                f.duration_minutes, f.base_price, f.currency,
                a.code AS airline_code, a.name AS airline_name,
                dep.code AS dep_code, arr.code AS arr_code,
                COUNT(fs.id) FILTER (WHERE fs.is_available = TRUE) AS available_seats
            FROM flights f
            JOIN airlines a ON f.airline_id = a.id
            JOIN airports dep ON f.departure_airport_id = dep.id
            JOIN airports arr ON f.arrival_airport_id = arr.id
            LEFT JOIN flight_seats fs ON f.id = fs.flight_id
            WHERE 
                f.departure_airport_id = $1
                AND f.arrival_airport_id = $2
                AND f.departure_time >= $3
                AND f.departure_time < $4
                AND f.is_active = TRUE
            GROUP BY f.id, a.code, a.name, dep.code, arr.code
            ORDER BY f.departure_time
            """,
            dep_airport['id'], arr_airport['id'], date_obj, next_day
        )
        return rows