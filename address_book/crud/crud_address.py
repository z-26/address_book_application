from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

from address_book.api.models.address_model import AddressBook

from address_book.api.schemas.address import AddressBookBase, AddressBookUpdate

from typing import Optional, List, Union, Dict, Any

import logging


logger = logging.getLogger(__name__)


class CRUDAddress():

    def get_by_id(self, db: Session, id: int) -> Optional[AddressBook]:
        logger.info(f"get_by_id is triggered")
        try:
            return db.query(AddressBook).filter(AddressBook.id == id).first()
        except Exception as e:
            logger.exception(f"Error occured in get_by_id : {e}")

    def get_all_addresses(self, db: Session) -> Optional[List[AddressBook]]:
        logger.info(f"get_all_addresses is triggered")
        try:
            return db.query(AddressBook).all()
        except Exception as e:
            logger.exception(f"Error occured in get_all_addresses : {e}")


    def create(self, db: Session, obj_in: AddressBookBase) -> Optional[AddressBook]:
        logger.info(f"create is triggered : {obj_in}")
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = AddressBook(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.exception(f"Error occured in create : {e}")
    
    def update(self, db: Session, *, db_obj: AddressBook, obj_in: Union[AddressBookUpdate, Dict[str, Any]]) -> AddressBook:
        logger.info(f"update is trigger: {obj_in}")
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
            obj_data = jsonable_encoder(db_obj)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.exception(f"Error occured in update : {e}")

    def delete(self, db: Session, id:int):
        logger.info("delete is trigger")
        try:
            obj_del = db.query(AddressBook).filter(AddressBook.id == id).first()
            if obj_del:
                db.delete(obj_del)
                db.commit()
                return True
            else:
                return False
        except Exception as e:
            logger.exception(f"Error occured in delete : {e}")


crud_address = CRUDAddress()