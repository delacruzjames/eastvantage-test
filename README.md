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

Create requires `latitude` (-90 to 90) and `longitude` (-180 to 180).
`distance` is a radius in kilometers. Nearby results are nearest first and
include `distance_km`.

### Sample curls

Health:

```bash
curl http://localhost:8000/health
```

Create:

```bash
curl -X POST http://localhost:8000/addresses \
  -H "Content-Type: application/json" \
  -d '{
    "street": "Rizal Park",
    "city": "Manila",
    "state": "NCR",
    "postal_code": "1000",
    "country": "Philippines",
    "latitude": 14.5826,
    "longitude": 120.9787
  }'
```

Find nearby (20 km from Rizal Park):

```bash
curl "http://localhost:8000/addresses?latitude=14.5826&longitude=120.9787&distance=20"
```

Update (send only the fields to change):

```bash
curl -X PATCH http://localhost:8000/addresses/1 \
  -H "Content-Type: application/json" \
  -d '{"street": "Rizal Park, Ermita"}'
```

Delete:

```bash
curl -X DELETE http://localhost:8000/addresses/1
```
