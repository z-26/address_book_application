from fastapi import APIRouter, Depends, Request, status
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from address_book.api import deps

from address_book.crud.crud_address import crud_address

from address_book.api.schemas.address import AddressBookBase, AddressBookUpdate

import logging

from typing import Optional

from datetime import datetime

from address_book.service.utils import generate_response, haversine
import address_book.service.response_msg as messages


router = APIRouter()


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)


@router.post("/address-book")
async def add_address(request: Request,
                      payload:AddressBookBase,
                      db: Session = Depends(deps.get_db)):
    '''
        This API will add the address of the user.
    '''
    logger.info(f"add_address is triggered....")
    try:
        if payload:
            address_data = crud_address.create(db=db, obj_in=payload)
            # putting the address coming in, into the db using the crud method - create 
            if address_data:
                return generate_response(status_code = status.HTTP_200_OK, message = messages.SUCCESS, data=[jsonable_encoder(address_data)])
            else:
                return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.ERROR, data=None)
        
        else:
            return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.ERROR)
    
    except Exception as e:
        logger.exception(f"Error occured in add_address : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)


@router.get("/all-address")
async def get_all_users_address(request: Request,
                                db: Session = Depends(deps.get_db)):
    '''
        This API will get the address of the all the users.
    '''
    logger.info(f"get_all_users_address is triggered....")
    try:
        address_book = crud_address.get_all_addresses(db=db)
        
        if address_book:
            return generate_response(status_code = status.HTTP_200_OK, message = messages.SUCCESS, data=jsonable_encoder(address_book))
        else:
            return generate_response(status_code = status.HTTP_404_NOT_FOUND, message = messages.DATA_NOT_FOUND, data=None)
    
    except Exception as e:
        logger.exception(f"Error occured in get_all_users_address : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)


@router.get("/address-book")
async def get_addresses_by_distance(request: Request,
                                    latitude: float,
                                    longitude: float,
                                    distance: float,
                                    db: Session = Depends(deps.get_db)):
    '''
        This API will get the addresses whose location coordinates are in the range of the distance provided by the user.
    '''
    logger.info(f"get_addresses_by_distance is triggered....")
    try:
        address_book = crud_address.get_all_addresses(db=db)
        response = []
        for address in address_book:
            actual_dist = haversine(lat1=address.latitude, lon1=address.longitude, lat2=latitude, lon2=longitude)
            if actual_dist < distance:
                # If the distance given by the API user is more than the haversine distance between the two location coordinates then it is in the range and will be displayed in the response
                address = jsonable_encoder(address)
                # making address a dict in order to put in the list
                response.append(address)
        return generate_response(status_code = status.HTTP_200_OK, message = messages.SUCCESS, data=response)
    except Exception as e:
        logger.exception(f"Error occured in get_addresses_by_distance : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)


@router.put("/address-book")
async def update_address(request:Request,
                         id: int,
                         payload: AddressBookUpdate,
                         db: Session = Depends(deps.get_db)):
    '''
        This API will update the address of the users by the id(PK).
    '''
    logger.info(f"update_address is triggered....")
    try:
        address = crud_address.get_by_id(db=db, id=id)
        if address:
            updated_address = crud_address.update(db=db, db_obj=address, obj_in=payload)
            if updated_address:
                return generate_response(status_code = status.HTTP_200_OK, message = messages.SUCCESS, data=[jsonable_encoder(updated_address)])
            else:
                return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.ERROR, data=None)
        else:
            return generate_response(status_code = status.HTTP_404_NOT_FOUND, message = messages.DATA_NOT_FOUND, data=None)
    
    except Exception as e:
        logger.exception(f"Error occured in update_address : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)


@router.delete("/address-book")
async def delete_address(request:Request,
                         id: int,
                         db: Session = Depends(deps.get_db)):
    '''
        This API will delete the address of the users by the id(PK).
    '''
    logger.info(f"delete_address is triggered....")
    try:
        deleted_address = crud_address.delete(db=db, id=id)
        if deleted_address == True:
            return generate_response(status_code = status.HTTP_200_OK, message = messages.SUCCESS)
        else:
            return generate_response(status_code = status.HTTP_404_NOT_FOUND, message = messages.DATA_NOT_FOUND)
    
    except Exception as e:
        logger.exception(f"Error occured in delete_address : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)

