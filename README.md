# Camunda Python Pipelines

A demo data pipeline orchestrated by [CIB seven](https://cibseven.org/) (a Camunda 7 distribution) and implemented as Python **external task workers**. A BPMN process drives three services that move a file from an S3 bucket, transform it, and upload the result to a second bucket.

## Pipeline flow

```
topic1 → topic2 → topic3
```

| Service | Topic | Container | Responsibility |
|---------|-------|-----------|----------------|
| `s3-fetcher-service`  | `topic1` | `service1` | Downloads the source file from S3 into `cache/<executionId>/` via rclone. |
| `handler-service`     | `topic2` | `service2` | Reads the JSON file and converts it to CSV (pandas). |
| `csv-uploader-service`| `topic3` | `service3` | Uploads the generated CSV to the `secondary-bucket` via rclone. |

Each worker subscribes to its topic, uses the process instance ID as the `executionId`, and shares the local `./cache` volume so files pass between steps.

## Components

- **cibseven** — workflow engine + web modeler, exposed on port `7080`.
- **postgres** — engine database (port `7432`).
- **alarik / console** — S3-compatible storage and its UI, on ports `8080` / `3000`.
- **service1–3** — the Python external task workers.

## Requirements

- Docker + Docker Compose
- An S3-compatible object store (the bundled `alarik` service, or any S3 endpoint)

## Configuration

Settings are provided through a `.env` file (git-ignored) at the repo root:

```env
CIB7_REST_URL=http://cibseven:8080/engine-rest
S3_ACCESS_KEY=<your-access-key>
S3_SECRET_KEY=<your-secret-key>
S3_ENDPOINT=http://alarik:8080
S3_REGION=us-east-1
```

The rclone remote is templated from `config/rclone.conf` at container startup (see each service's `entrypoint.sh`), which substitutes the `S3_*` variables into a working config.

Per-worker behavior is set in `compose.yml` via `TOPIC`, `WORKER_ID`, `FAILURE_RETRIES`, and `FAILURE_RETRY_TIMEOUT_MS`.

## Running

```bash
docker compose up --build
```

Then open the CIB seven web app at http://localhost:7080 to deploy/start a process, and the storage console at http://localhost:3000.

The process must set a `sourcePath` variable (the rclone path to the source file) that `topic1` uses to fetch the input.

## Project structure

```
.
├── compose.yml            # Full stack: engine, DB, storage, workers
├── config/rclone.conf     # rclone remote template (S3_* placeholders)
├── mock_data.json         # Sample input data
├── cache/                 # Per-execution working files (git-ignored)
└── services/
    ├── service1/          # S3 fetcher  (rclone)
    ├── service2/          # JSON → CSV  (pandas)
    └── service3/          # CSV uploader (rclone)
```
