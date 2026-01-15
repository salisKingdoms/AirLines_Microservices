from datetime import datetime
#from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID

class AirlineResponse (BaseModel):
    id : UUID
    name : str
    code : str
    logo_url : str
    country : str
    founded_year : int
    is_active : bool
    created_at : datetime
    updated_at : datetime