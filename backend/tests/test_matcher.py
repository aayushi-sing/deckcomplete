from app.core.matcher import build_collection, match_all, match_deck
from app.core.models import DeckCard, Decklist, ParsedCardLine


def card(name, quantity):
    return ParsedCardLine(quantity=quantity, name=name)


def deck(name, *entries):
    return Decklist(
        name=name,
        cards=[DeckCard(name=n, quantity=q) for n, q in entries],
    )


def test_build_collection_adds_up_duplicate_names():
    collection = build_collection(
        [card("Pikachu", 2), card("Pikachu", 1), card("Raichu", 1)]
    )
    assert collection == {"pikachu": 3, "raichu": 1}


def test_build_collection_ignores_case_and_extra_spaces():
    collection = build_collection([card("Pikachu", 1), card("  pikachu ", 2)])
    assert collection == {"pikachu": 3}


def test_full_match_is_100_percent_with_nothing_missing():
    d = deck("Test Deck", ("Pikachu", 4), ("Raichu", 2))
    result = match_deck({"pikachu": 4, "raichu": 2}, d)
    assert result.total_cards == 6
    assert result.owned_cards == 6
    assert result.percent_owned == 100.0
    assert result.missing == []


def test_partial_match_lists_missing_cards():
    d = deck("Test Deck", ("Pikachu", 4), ("Raichu", 2))
    result = match_deck({"pikachu": 3}, d)
    assert result.owned_cards == 3
    assert result.total_cards == 6
    assert result.percent_owned == 50.0
    missing = {m.name: (m.needed, m.owned) for m in result.missing}
    assert missing == {"Pikachu": (4, 3), "Raichu": (2, 0)}


def test_extra_copies_do_not_count_beyond_what_the_deck_needs():
    d = deck("Test Deck", ("Pikachu", 2))
    result = match_deck({"pikachu": 10}, d)
    assert result.owned_cards == 2
    assert result.percent_owned == 100.0


def test_missing_cards_use_the_decklist_spelling():
    d = deck("Test Deck", ("Professor's Research", 4))
    result = match_deck({}, d)
    assert result.missing[0].name == "Professor's Research"
    assert result.owned_cards == 0
    assert result.percent_owned == 0.0


def test_empty_decklist_does_not_crash():
    result = match_deck({"pikachu": 1}, deck("Empty"))
    assert result.total_cards == 0
    assert result.percent_owned == 0.0


def test_percent_is_rounded_to_one_decimal():
    d = deck("Test Deck", ("Pikachu", 3))
    result = match_deck({"pikachu": 1}, d)
    assert result.percent_owned == 33.3


def test_match_all_sorts_best_match_first_then_by_name():
    decks = [
        deck("B Deck", ("Pikachu", 2)),
        deck("A Deck", ("Pikachu", 2)),
        deck("C Deck", ("Raichu", 2)),
    ]
    results = match_all({"pikachu": 2}, decks)
    assert [r.deck_name for r in results] == ["A Deck", "B Deck", "C Deck"]
