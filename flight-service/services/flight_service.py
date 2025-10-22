from repositories.flight_repository import FlightRepository
from repositories.seat_repository import SeatRepository

class FlightService:
    def __init__(self, flight_repo: FlightRepository, seat_repo: SeatRepository):
        self.flight_repo = flight_repo
        self.seat_repo = seat_repo

    async def search_flights(self, criteria):
        return await self.flight_repo.search_flights(
            criteria.departure_airport,
            criteria.arrival_airport,
            criteria.departure_date
        )

    async def reserve_seats(self, flight_id: str, seat_numbers: list[str], user_id: str) -> bool:
        return await self.seat_repo.lock_and_reserve_seats(flight_id, seat_numbers, user_id)