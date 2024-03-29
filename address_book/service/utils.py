from fastapi import status

import logging

import math

from typing import Optional

import address_book.service.response_msg as messages

from address_book.api.schemas.generic_response import Response


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_response(status_code=status.HTTP_200_OK, message=messages.SUCCESS, data=[])->Optional[Response]:
    """
        Generic response function, can be used in all the return statements
    """
    logger.info("generate_response is triggered")
    try:
        return Response(status_code=status_code,
                                data=data,
                                message=message)
    except Exception as e:
        logger.exception(f"Error occurred in generate_response:{e}")


def haversine(lat1, lon1, lat2, lon2):
    """
        Calculate the great circle distance between two points on the earth specified in decimal degrees.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km