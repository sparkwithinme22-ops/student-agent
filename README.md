# Student VISOLACE Agent

## Purpose

This Level 1 project demonstrates the technical contract of an agent without an
AI model. It receives a text task over HTTP, validates it, processes it, and
returns a structured JSON result containing word and character counts.

## Requirements

- Python 3.12 or 3.13
- `pip`
- Docker Desktop (for the container workflow)
- Git

The workstation verification record is in [`SETUP.md`](SETUP.md).

## Installation

From PowerShell in the project directory:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On macOS or Linux, create and activate the environment with an installed Python
3.12 interpreter:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run locally

```bash
python -m uvicorn app.main:app --reload --port 8080
```

Open <http://localhost:8080/docs> for FastAPI's interactive Swagger UI. Stop
the service with `Ctrl+C`.

## Run tests

```bash
python -m pytest -v
```

## Run with Docker

Build and start the image:

```bash
docker build -t student-agent:0.1.0 .
docker run --name student-agent -p 8080:8080 student-agent:0.1.0
```

In another terminal, test the health endpoint:

```bash
curl http://localhost:8080/health
```

View or stop the container:

```bash
docker logs student-agent
docker stop student-agent
docker rm student-agent
```

## API

### `GET /health`

Reports whether the service is running.

```json
{"status": "healthy"}
```

### `GET /identity`

Describes the agent.

```json
{
  "agent_id": "student-agent",
  "name": "Student VISOLACE Agent",
  "version": "0.1.0"
}
```

### `POST /task`

Accepts a task ID and non-empty text. Text is limited to 10,000 characters and
task IDs are limited to 100 characters.

## Example request

```bash
curl -X POST http://localhost:8080/task \
  -H "Content-Type: application/json" \
  -d '{"task_id":"task-001","text":"Hello VISOLACE"}'
```

PowerShell alternative:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8080/task `
  -ContentType "application/json" `
  -Body '{"task_id":"task-001","text":"Hello VISOLACE"}'
```

## Example response

```json
{
  "task_id": "task-001",
  "status": "completed",
  "result": {
    "original_text": "Hello VISOLACE",
    "word_count": 2,
    "character_count": 14
  }
}
```

Invalid JSON or missing, incorrectly typed, empty, or whitespace-only fields
return HTTP `400` with a structured error response.

## Known limitations

- The agent does not use an AI model.
- Tasks are processed synchronously and are not stored.
- Authentication and rate limiting are not implemented in Level 1.
- Character count uses Python string length; Unicode characters count as code
  points rather than visible grapheme clusters.
