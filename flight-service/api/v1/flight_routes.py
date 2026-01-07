from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from repositories.flight_repository import FlightRepository
from repositories.seat_repository import SeatRepository
from services.flight_service import FlightService
from models.flight import FlightSearchRequest,FlightResponse
from typing import List
from datetime import timedelta

router = APIRouter(prefix="/api/v1/flights", tags=["flights"])

#@router.post("/search")--old

@router.post(
    "/search",
    response_model=dict[str, list[FlightResponse]]
)
async def search_flights(request: FlightSearchRequest, conn=Depends(get_db)):
    repo = FlightRepository(conn)
    service = FlightService(repo, SeatRepository(conn))
    flights = await service.search_flights(request)
    return {
        "flights": [
            FlightResponse(
                id=f['id'],
                flight_number=f['flight_number'],
                airline_code=f['airline_code'],
                airline_name=f['airline_name'],
                departure_airport=f['dep_code'],
                arrival_airport=f['arr_code'],
                departure_time=f['departure_time'],
                arrival_time=f['arrival_time'],
                duration_times=f['duration_times'],  # timedelta
                duration_times_str=format_duration(f['duration_times']), 
                duration_minutes=f['duration_minutes'],
                base_price=float(f['base_price']),
                currency=f['currency'],
                available_seats=f['available_seats']
            )
            for f in flights
        ]
    }
    # return {
    #     "flights": [
    #         {
    #             "id": str(f['id']),
    #             "flight_number": f['flight_number'],
    #             "airline_code": f['airline_code'],
    #             "airline_name": f['airline_name'],
    #             "departure_airport": f['dep_code'],
    #             "arrival_airport": f['arr_code'],
    #             "departure_time": f['departure_time'],
    #             "arrival_time": f['arrival_time'],
    #             "duration_times": f['duration_times'],
    #             "duration_minutes": f['duration_minutes'],
    #             "base_price": float(f['base_price']),
    #             #"currency": f['currency'],
    #             "available_seats": f['available_seats']
    #         }
    #         for f in flights
    #     ]
    # }

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

def format_duration(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02}:{m:02}:{s:02}"
