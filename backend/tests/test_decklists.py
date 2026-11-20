import json

from app.decklists import load_decklists


def test_load_decklists_reads_json_files(tmp_path):
    data = {"name": "A", "cards": [{"name": "Pikachu", "quantity": 4}]}
    (tmp_path / "a.json").write_text(json.dumps(data), encoding="utf-8")
    decks = load_decklists(tmp_path)
    assert [d.name for d in decks] == ["A"]
    assert decks[0].cards[0].quantity == 4


def test_load_decklists_returns_empty_list_for_empty_folder(tmp_path):
    assert load_decklists(tmp_path) == []


def test_load_decklists_returns_empty_list_for_missing_folder(tmp_path):
    assert load_decklists(tmp_path / "does-not-exist") == []
