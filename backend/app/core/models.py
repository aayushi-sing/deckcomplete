from pydantic import BaseModel, Field


class ParsedCardLine(BaseModel):
    quantity: int = Field(gt=0)
    name: str = Field(min_length=1)
    set_code: str | None = None
    number: str | None = None


class UnrecognizedLine(BaseModel):
    line_number: int = Field(ge=1)
    text: str
    reason: str = Field(min_length=1)


class ParseResult(BaseModel):
    cards: list[ParsedCardLine]
    unrecognized_lines: list[UnrecognizedLine]


class DeckCard(BaseModel):
    name: str = Field(min_length=1)
    quantity: int = Field(gt=0)


class Decklist(BaseModel):
    name: str
    cards: list[DeckCard]


class MissingCard(BaseModel):
    name: str
    needed: int
    owned: int


class DeckMatch(BaseModel):
    deck_name: str
    owned_cards: int
    total_cards: int
    percent_owned: float
    missing: list[MissingCard]


class AnalysisResult(BaseModel):
    unrecognized_lines: list[UnrecognizedLine]
    matches: list[DeckMatch]
