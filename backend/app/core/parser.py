import re

from app.core.models import ParsedCardLine


_QUANTITY_PATTERN = re.compile(
    r"(?P<quantity>[1-9][0-9]*)[ \t]+(?P<body>\S[^\r\n]*)"
)
_PRINTING_PATTERN = re.compile(
    r"(?P<name>.+?)[ \t]+(?P<set_code>[A-Z][A-Z0-9]*)[ \t]+(?P<number>[0-9]+)"
)


def parse_line(line: str) -> ParsedCardLine | None:
    match = _QUANTITY_PATTERN.fullmatch(line.strip())
    if match is None:
        return None

    quantity = int(match.group("quantity"))
    body = match.group("body")
    printing = _PRINTING_PATTERN.fullmatch(body)
    if printing is not None:
        return ParsedCardLine(
            quantity=quantity,
            name=printing.group("name").strip(),
            set_code=printing.group("set_code"),
            number=printing.group("number"),
        )

    return ParsedCardLine(quantity=quantity, name=body)
