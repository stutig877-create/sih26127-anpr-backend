from sqlalchemy.orm import Session
from app.database.models import Blacklist


class BlacklistService:
    def __init__(self, db: Session):
        self.db = db

    def list_blacklists(self):
        return self.db.query(Blacklist).order_by(Blacklist.id).all()

    def get_blacklist(self, blacklist_id: int):
        return self.db.query(Blacklist).filter(Blacklist.id == blacklist_id).first()

    def get_blacklist_by_plate(self, plate_number: str):
        return self.db.query(Blacklist).filter(
            Blacklist.plate_number == plate_number.strip().upper()
        ).first()

    def create_blacklist(self, plate_number: str, reason: str = None, created_by: str = None):
        record = Blacklist(
            plate_number=plate_number,
            reason=reason,
            created_by=created_by,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def update_blacklist(self, blacklist: Blacklist, **kwargs):
        for field, value in kwargs.items():
            if value is not None:
                setattr(blacklist, field, value)
        self.db.commit()
        self.db.refresh(blacklist)
        return blacklist

    def delete_blacklist(self, blacklist: Blacklist):
        self.db.delete(blacklist)
        self.db.commit()
        return True
