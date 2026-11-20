import pytest
from fastapi.testclient import TestClient

from app.core.models import DeckCard, Decklist
from app.main import app, get_decklists

SAMPLE = [
    Decklist(
        name="Sample Deck",
        cards=[
            DeckCard(name="Pikachu", quantity=4),
            DeckCard(name="Raichu", quantity=2),
        ],
    )
]


@pytest.fixture
def client():
    app.dependency_overrides[get_decklists] = lambda: SAMPLE
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_match_returns_matches_for_owned_cards(client):
    response = client.post("/match", json={"text": "4 Pikachu\n1 Raichu"})
    assert response.status_code == 200
    body = response.json()
    assert body["unrecognized_lines"] == []
    assert len(body["matches"]) == 1
    match = body["matches"][0]
    assert match["deck_name"] == "Sample Deck"
    assert match["owned_cards"] == 5
    assert match["total_cards"] == 6
    assert match["percent_owned"] == 83.3
    assert match["missing"] == [{"name": "Raichu", "needed": 2, "owned": 1}]


def test_match_reports_unrecognized_lines(client):
    response = client.post("/match", json={"text": "4 Pikachu\nnot a card"})
    assert response.status_code == 200
    flagged = response.json()["unrecognized_lines"][0]
    assert flagged["line_number"] == 2
    assert flagged["text"] == "not a card"


def test_match_rejects_a_request_without_text(client):
    response = client.post("/match", json={})
    assert response.status_code == 422


def test_match_with_empty_text_owns_nothing(client):
    response = client.post("/match", json={"text": ""})
    assert response.status_code == 200
    assert response.json()["matches"][0]["owned_cards"] == 0
