from fastapi import FastAPI

app = FastAPI(title="DeckComplete API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}