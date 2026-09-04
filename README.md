# EastVantage Test API

FastAPI + SQLite REST API with Swagger UI. Run it locally with Docker.

## Make shortcuts

```bash
make help          # list commands
make install       # create .venv and install deps
make run           # run API locally (reload)
make test          # run tests
make migrate       # apply alembic migrations
make docker-up     # docker compose up --build
make docker-down   # docker compose down
```

## Quick start (Docker)

Make sure Docker Desktop (or Colima) is running, then:

```bash
make docker-up
```

Then open:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

Stop the stack with `Ctrl+C` or `docker compose down`.

SQLite data is stored in a Docker volume (`sqlite-data`).

## Run without Docker

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Tests

```bash
make test
```

## Migrations

```bash
make migrate
```

Create a new revision after model changes:

```bash
.venv/bin/alembic revision --autogenerate -m "describe the change"
```

## API

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Health check |
| GET | `/addresses` | Find addresses within a distance of a coordinate |
| POST | `/addresses` | Create an address |
| PATCH | `/addresses/{id}` | Update an address |
| DELETE | `/addresses/{id}` | Delete an address |

### Find addresses near a coordinate

Create and update validate coordinates (`latitude` -90 to 90, `longitude` -180
to 180). Create requires both coordinates.

`distance` is a radius in kilometers. Results are sorted from nearest to
farthest and include the calculated `distance_km`.

```bash
curl "http://localhost:8000/addresses?latitude=14.5826&longitude=120.9787&distance=20"
```
