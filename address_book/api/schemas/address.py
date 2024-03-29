from pydantic import BaseModel, validator

from typing import Optional


class AddressBookBase(BaseModel):
    latitude: float
    longitude: float
    user_email: str
    user_name: Optional[str]
    
    @validator('latitude')
    def validate_and_check_latitude(cls, v):
        if not isinstance(v, float):
            raise ValueError('Only float values are allowed')
        if not -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90 degrees')
        return v
    
    @validator('longitude')
    def validate_and_check_longitude(cls, v):
        if not isinstance(v, float):
            raise ValueError('Only float values are allowed')
        if not -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180 degrees')
        return v


class AddressBookUpdate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    
    @validator('latitude')
    def validate_and_check_latitude(cls, v):
        if not isinstance(v, float):
            raise ValueError('Only float values are allowed')
        if not -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90 degrees')
        return v
    
    @validator('longitude')
    def validate_and_check_longitude(cls, v):
        if not isinstance(v, float):
            raise ValueError('Only float values are allowed')
        if not -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180 degrees')
        return v
