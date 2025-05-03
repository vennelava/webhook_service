from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import engine, SessionLocal
from app.api.routes import router as ingest_router  # Updated import for routes

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Root endpoint with styled HTML message
@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Webhook Service</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #B2D8E3, #F1F7FB);
                color: #333;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                padding: 20px;
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                max-width: 400px;
                width: 100%;
            }
            h1 {
                font-size: 2.5rem;
                color: #2E3B4E;
                margin-bottom: 15px;
            }
            p {
                font-size: 1.2rem;
                color: #4A5568;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the Webhook Service!</h1>
            <p>Thank you for visiting. This is your webhook endpoint.</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Subscription CRUD endpoints
@app.post("/subscriptions/")
def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    return crud.create_subscription(db=db, subscription=subscription)

@app.get("/subscriptions/")
def read_subscriptions(db: Session = Depends(get_db)):
    return crud.get_subscriptions(db=db)

@app.get("/subscriptions/{subscription_id}")
def read_subscription(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = crud.get_subscription(db, subscription_id=subscription_id)
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription

@app.put("/subscriptions/{subscription_id}")
def update_subscription(subscription_id: int, subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    return crud.update_subscription(db=db, subscription_id=subscription_id, subscription=subscription)

@app.delete("/subscriptions/{subscription_id}")
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    return crud.delete_subscription(db=db, subscription_id=subscription_id)

# 🚀 Webhook ingestion route
app.include_router(ingest_router)
