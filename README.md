This is a webhook delivery service that processes incoming webhooks, supports subscription management, and ensures reliable delivery with retries and logging. The service is built using FastAPI, PostgreSQL, and Docker. It is designed for scalable and asynchronous processing of webhook events.

TECH STACK

Backend: FastAPI
Database: PostgreSQL
Containerization: Docker & Docker Compose
API Documentation: Swagger UI
Environment Management: .env file

INSTALLATION

prerequisites
make sure you have Docker, Docker Compose, Python installed

Local setup using Docker
1.clone repository:
git clone https://github.com/vennelava/webhook_service.git

cd webhook_service

2.set up the docker containers:
docker-compose up --build

access the app:
The service will be running at http://localhost:8000.
You can test the API using Swagger UI by navigating to http://localhost:8000/docs

Running locally without Docker
1.create and activate virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

2.install the dependencies:
pip install -r requirements.txt

3.run the FastAPI app:
uvicorn app.main:app --reload

DEPLOYMENT

The project is deployed on Render and can be accessed here:
https://webhook-service-thn5.onrender.com

API documentation is available at:
https://webhook-service-thn5.onrender.com/docs

SAMPLE CURL OPERATIONS

1. create subscription
curl -X POST http://localhost:8000/subscriptions/ \
-H "Content-Type: application/json" \
-d '{
  "url": "https://example.com/webhook",
  "secret": "mysecret",
  "event_type": "user_signup"
}'

2. update subscription
curl -X PUT http://localhost:8000/subscriptions/1 \
-H "Content-Type: application/json" \
-d '{
  "url": "https://example.com/updated",
  "secret": "newsecret",
  "event_type": "user_login"
}'

3. list all subscriptions
curl http://localhost:8000/subscriptions/

4. get subscription id
curl http://localhost:8000/subscriptions/1

5. delete subscription
curl -X DELETE http://localhost:8000/subscriptions/1

6. ingest webhook
curl -X POST http://localhost:8000/ingest_event \
-H "Content-Type: application/json" \
-d '{
  "event_type": "user_signup",
  "payload": {
    "user_id": 123,
    "timestamp": "2025-05-03T10:00:00Z"
  }
}'


Estimated cost:

Assumes moderate usage (~5,000 events/day), each triggering ~1.2 deliveries on average. The free tier comfortably handles this with occasional cold starts and retry spikes.

Assumptions

Delivery endpoints (client URLs) will accept JSON payloads over POST.
Secrets are shared in advance and known only between sender and receiver.
A retry limit of 3 is sufficient for most transient delivery failures.
No payload validation or signature verification on the receiver side (but secret is available if needed).

CREDITS

FastAPI

Celery

Redis

Render

Docker

OpenAI ChatGPT – for helping break down and guide the architecture and implementation
