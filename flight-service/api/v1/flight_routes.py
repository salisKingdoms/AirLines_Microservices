from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from repositories.flight_repository import FlightRepository
from repositories.seat_repository import SeatRepository
from services.flight_service import FlightService
from models.flight import FlightSearchRequest

router = APIRouter(prefix="/api/v1/flights", tags=["flights"])

@router.post("/search")
async def search_flights(request: FlightSearchRequest, conn=Depends(get_db)):
    repo = FlightRepository(conn)
    service = FlightService(repo, SeatRepository(conn))
    flights = await service.search_flights(request)
    return {
        "flights": [
            {
                "flight_id": str(f['id']),
                "flight_number": f['flight_number'],
                "airline_code": f['airline_code'],
                "airline_name": f['airline_name'],
                "departure_airport": f['dep_code'],
                "arrival_airport": f['arr_code'],
                "departure_time": f['departure_time'],
                "arrival_time": f['arrival_time'],
                "duration_minutes": f['duration_minutes'],
                "base_price": float(f['base_price']),
                "currency": f['currency'],
                "available_seats": f['available_seats']
            }
            for f in flights
        ]
    }

@router.post("/reserve")
async def reserve_seats(
    flight_id: str,
    seat_numbers: list[str],
    user_id: str,  # In real app, get from JWT
    conn=Depends(get_db)
):
    if not seat_numbers:
        raise HTTPException(400, "At least one seat must be selected")
    repo = FlightRepository(conn)
    seat_repo = SeatRepository(conn)
    service = FlightService(repo, seat_repo)
    success = await service.reserve_seats(flight_id, seat_numbers, user_id)
    if not success:
        raise HTTPException(409, "One or more seats are no longer available")
    return {"status": "reserved", "seats": seat_numbers}