from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from app.core.analyze import analyze
from app.core.models import AnalysisResult, Decklist
from app.decklists import load_decklists

app = FastAPI(title="DeckComplete API")


class MatchRequest(BaseModel):
    text: str


def get_decklists() -> list[Decklist]:
    return load_decklists(Path(__file__).parent / "data" / "decklists")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/match", response_model=AnalysisResult)
def match(
    request: MatchRequest,
    decklists: Annotated[list[Decklist], Depends(get_decklists)],
) -> AnalysisResult:
    return analyze(request.text, decklists)
