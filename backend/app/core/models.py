from pydantic import BaseModel, Field


class ParsedCardLine(BaseModel):
    quantity: int = Field(gt=0)
    name: str = Field(min_length=1)
    set_code: str | None = None
    number: str | None = None
