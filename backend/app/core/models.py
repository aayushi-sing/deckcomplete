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
