from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class FlightSearchRequest(BaseModel):
    departure_airport: str
    arrival_airport: str
    departure_date: str  # YYYY-MM-DD
    passenger_count: int = 1

class SeatInfo(BaseModel):
    seat_number: str
    seat_class: str
    price: float
    is_available: bool

class FlightResponse(BaseModel):
    flight_id: str
    flight_number: str
    airline_code: str
    airline_name: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    base_price: float
    currency: str
    available_seats: int