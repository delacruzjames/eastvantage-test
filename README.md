# EastVantage Test API

FastAPI + SQLite address book API. Swagger is at `/docs`.

## How to run (Makefile)

From the project folder:

```bash
cd eastvantage-test
make install
make migrate
make run
```

Then open:

- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health

Stop the server with `Ctrl+C`.

If you just cloned the repo:

```bash
git clone https://github.com/delacruzjames/eastvantage-test.git
cd eastvantage-test
make install
make migrate
make run
```

## Make commands

```bash
make help          # list commands
make install       # create .venv and install deps
make run           # start the API with reload
make migrate       # apply database migrations
make test          # run tests
make docker-up     # run with Docker Compose
make docker-down   # stop Docker Compose
```

## Docker

Docker Desktop (or Colima) must be running:

```bash
cd eastvantage-test
make docker-up
```

SQLite data is stored in a Docker volume (`sqlite-data`). Stop with `Ctrl+C` or `make docker-down`.

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
