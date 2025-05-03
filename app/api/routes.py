from fastapi import APIRouter, Request, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.crud import get_subscriptions_by_event
from app.database import get_db
from app.delivery import deliver_webhook_with_retries
import hmac
import hashlib
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter()

@router.post("/ingest_event")
async def ingest_event(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        body = await request.json()
        event_type = request.headers.get("X-Event-Type")

        if not event_type:
            raise HTTPException(status_code=400, detail="Missing X-Event-Type header")

        subscriptions = get_subscriptions_by_event(db, event_type)

        if not subscriptions:
            logger.warning(f"No subscriptions found for event type {event_type}")

        body_str = json.dumps(body, separators=(",", ":"))  # Consistent JSON for HMAC

        for sub in subscriptions:
            signature = request.headers.get("X-Signature")
            if not signature:
                raise HTTPException(status_code=400, detail="Missing signature header")

            expected_signature = hmac.new(
                sub.secret.encode("utf-8"),
                body_str.encode("utf-8"),
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(signature, expected_signature):
                raise HTTPException(status_code=400, detail="Invalid signature")

        for sub in subscriptions:
            background_tasks.add_task(deliver_webhook_with_retries, sub.callback_url, body, sub.secret)

        logger.info(f"Webhooks scheduled for background delivery for event {event_type}")
        return {"status": "Webhooks scheduled"}
    
    except Exception as e:
        logger.error(f"Error ingesting event: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
