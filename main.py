"""HTTP API for the Level 1 Hello VISOLACE Agent."""

import logging
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("student-agent")

app = FastAPI(
    title="Student VISOLACE Agent",
    description="A Level 1 agent that analyzes text without using an AI model.",
    version="0.1.0",
)


class TaskRequest(BaseModel):
    """Input contract for a text-processing task."""

    task_id: str = Field(min_length=1, max_length=100)
    text: str = Field(min_length=1, max_length=10_000)

    @field_validator("task_id", "text")
    @classmethod
    def reject_whitespace_only(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be empty or contain only whitespace")
        return value


class TaskResult(BaseModel):
    original_text: str
    word_count: int
    character_count: int


class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: TaskResult


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Return the assignment's requested 400 response for invalid input."""
    logger.warning("Invalid request for %s: %s", request.url.path, exc.errors())
    errors = [
        {
            "field": ".".join(str(part) for part in error["loc"] if part != "body"),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=400,
        content={"status": "error", "message": "Invalid request", "errors": errors},
    )


@app.get("/health")
def health() -> Dict[str, str]:
    """Report whether the service is available."""
    return {"status": "healthy"}


@app.get("/identity")
def identity() -> Dict[str, str]:
    """Describe this agent and its API version."""
    return {
        "agent_id": "student-agent",
        "name": "Student VISOLACE Agent",
        "version": "0.1.0",
    }


@app.post("/task", response_model=TaskResponse)
def process_task(task: TaskRequest) -> TaskResponse:
    """Count the words and characters in the supplied text."""
    logger.info("Task %s received", task.task_id)
    logger.info("Processing task %s started", task.task_id)

    result = TaskResult(
        original_text=task.text,
        word_count=len(task.text.split()),
        character_count=len(task.text),
    )

    logger.info("Task %s completed", task.task_id)
    return TaskResponse(task_id=task.task_id, status="completed", result=result)
