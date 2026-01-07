import asyncpg

class SeatRepository:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def lock_and_reserve_seats(self, flight_id: str, seat_numbers: list[str], user_id: str) -> bool:
        """
        Use SELECT FOR UPDATE to prevent double-booking under high concurrency.
        Returns True if all seats were available and reserved.
        """
        placeholders = ', '.join(f'${i+1}' for i in range(len(seat_numbers)))
        query = f"""
            UPDATE seats 
            SET is_available = FALSE, updated_at = NOW()
            WHERE flight_id = $1 
              AND seat_number = ANY(ARRAY[{placeholders}])
              AND is_available = TRUE
            RETURNING id
        """
        args = [flight_id] + seat_numbers
        result = await self.conn.fetch(query, *args)
        return len(result) == len(seat_numbers)