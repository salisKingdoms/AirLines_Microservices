from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel,field_serializer
from uuid import UUID

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
    id: UUID
    flight_number: str
    airline_code: str
    airline_name: str
    departure_airport: str
    arrival_airport: str
    arrival_time: datetime
    duration_times: timedelta
    duration_minutes: int
    base_price: float
    currency: str
    available_seats: int
    
    @field_serializer("duration_times")
    def serialize_duration_time(self, value: timedelta) -> str:
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"