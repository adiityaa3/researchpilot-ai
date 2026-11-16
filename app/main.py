import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.agent import run_research

logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Research Agent",
    description="Research assistant powered by OpenAI and Tavily",
    version="1.0.0"
)


class ResearchRequest(BaseModel):
    query: str = Field(
        min_length=5,
        max_length=500,
        description="Enter a topic to research"
    )


@app.get("/")
def home():
    return {
        "message": "AI Research Agent is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/research")
def research(request: ResearchRequest):
    try:
        return run_research(request.query)

    except Exception:
        logger.exception("Research workflow failed")

        raise HTTPException(
            status_code=502,
            detail="Research failed. Check application logs."
        )