from fastapi import APIRouter, Depends, HTTPException, status, Query
from database import get_db
from repositories.flight_repository import FlightRepository
from repositories.seat_repository import SeatRepository
from repositories.airline_repository import AirlineRepository
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

#name: str| None, code: str | None, is_active: bool | None, page: int=1, page_size: int = 10
@router.get("/airlines")
async def get_airline_list(
    airline_name: str|None = Query(
        default=None,
        description="filter by airline name"
    ),
    airline_code: str|None = Query(
        default=None,
        description="filter by airline code"
    ),
    is_active: bool|None = Query(
        default=None,
        description="filter by active status"
    ),
    page : int = Query(
        default=1,
        ge=1,
        description="Page Number"
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Item per page"
    ),
    conn=Depends(get_db),
):
    repo = AirlineRepository(conn)

    rows = await repo.search_airlines(
        name=airline_name,
        code=airline_code,
        is_active=is_active,
        page=page,
        page_size=page_size
    )

    return {
        "page": page,
        "page_size" : page_size,
        "data" : rows
    }