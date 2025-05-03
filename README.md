This is a webhook delivery service that processes incoming webhooks, supports subscription management, and ensures reliable delivery with retries and logging. The service is built using FastAPI, PostgreSQL, and Docker. It is designed for scalable and asynchronous processing of webhook events.

TECH STACK
Backend: FastAPI
Database: PostgreSQL
Containerization: Docker & Docker Compose
API Documentation: Swagger UI
Environment Management: .env file

INSTALLATION

prerequisites
make sure youhave Docker, Docker Compose, Python installed

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


