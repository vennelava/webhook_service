from sqlalchemy.orm import Session
from . import models, schemas

def create_subscription(db: Session, sub: schemas.SubscriptionCreate):
    db_sub = models.Subscription(**sub.dict())
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

def get_subscriptions(db: Session):
    return db.query(models.Subscription).all()

def get_subscriptions_by_event(db: Session, event: str):
    return db.query(models.Subscription).filter(models.Subscription.event == event).all()
