from app.core.models import Decklist, DeckMatch, MissingCard, ParsedCardLine


def build_collection(cards: list[ParsedCardLine]) -> dict[str, int]:
    collection: dict[str, int] = {}
    for card in cards:
        name = card.name.strip().casefold()
        collection[name] = collection.get(name, 0) + card.quantity
    return collection


def match_deck(collection: dict[str, int], deck: Decklist) -> DeckMatch:
    normalized_collection: dict[str, int] = {}
    for name, quantity in collection.items():
        normalized = name.strip().casefold()
        normalized_collection[normalized] = (
            normalized_collection.get(normalized, 0) + quantity
        )

    requirements: dict[str, int] = {}
    spellings: dict[str, str] = {}
    for card in deck.cards:
        name = card.name.strip().casefold()
        requirements[name] = requirements.get(name, 0) + card.quantity
        spellings.setdefault(name, card.name)

    total_cards = sum(requirements.values())
    owned_cards = 0
    missing: list[MissingCard] = []
    for name, needed in requirements.items():
        owned = normalized_collection.get(name, 0)
        owned_cards += min(owned, needed)
        if owned < needed:
            missing.append(
                MissingCard(name=spellings[name], needed=needed, owned=owned)
            )

    percent_owned = round(owned_cards / total_cards * 100, 1) if total_cards else 0.0
    return DeckMatch(
        deck_name=deck.name,
        owned_cards=owned_cards,
        total_cards=total_cards,
        percent_owned=percent_owned,
        missing=missing,
    )


def match_all(collection: dict[str, int], decks: list[Decklist]) -> list[DeckMatch]:
    matches = [match_deck(collection, deck) for deck in decks]
    return sorted(matches, key=lambda match: (-match.percent_owned, match.deck_name))
