from app.core.parser import parse_list


def names(result):
    return [card.name for card in result.cards]


def test_valid_cards_are_returned_in_order():
    result = parse_list("4 Pikachu\n2 Raichu")
    assert names(result) == ["Pikachu", "Raichu"]
    assert result.unrecognized_lines == []


def test_unreadable_line_between_valid_cards_is_flagged_not_dropped():
    result = parse_list("4 Pikachu\nthis is not a card\n2 Raichu")
    assert names(result) == ["Pikachu", "Raichu"]
    assert len(result.unrecognized_lines) == 1
    flagged = result.unrecognized_lines[0]
    assert flagged.line_number == 2
    assert flagged.text == "this is not a card"
    assert flagged.reason != ""


def test_blank_lines_and_known_headers_are_not_flagged():
    text = (
        "Pokémon: 2\n"
        "2 Pikachu\n"
        "\n"
        "Trainer: 1\n"
        "1 Iono SVI 185\n"
        "\n"
        "Energy: 0\n"
        "Total Cards: 3"
    )
    result = parse_list(text)
    assert names(result) == ["Pikachu", "Iono"]
    assert result.unrecognized_lines == []


def test_header_without_accent_is_not_flagged():
    result = parse_list("Pokemon: 1\n1 Pikachu")
    assert names(result) == ["Pikachu"]
    assert result.unrecognized_lines == []


def test_unknown_header_like_line_is_flagged():
    result = parse_list("Stadium: 2\n2 Pikachu")
    assert names(result) == ["Pikachu"]
    assert len(result.unrecognized_lines) == 1
    assert result.unrecognized_lines[0].text == "Stadium: 2"


def test_line_numbers_count_blank_lines():
    result = parse_list("\n\nnot a card\n")
    assert len(result.unrecognized_lines) == 1
    assert result.unrecognized_lines[0].line_number == 3


def test_original_text_of_flagged_line_is_preserved():
    result = parse_list("  ???  ")
    assert result.unrecognized_lines[0].text == "  ???  "


def test_windows_line_endings_work():
    result = parse_list("4 Pikachu\r\n2 Raichu\r\n")
    assert names(result) == ["Pikachu", "Raichu"]
    assert result.unrecognized_lines == []


def test_empty_text_returns_an_empty_result():
    result = parse_list("")
    assert result.cards == []
    assert result.unrecognized_lines == []


def test_duplicate_lines_are_kept_separately():
    result = parse_list("2 Pikachu SVI 1\n2 Pikachu SVI 1")
    assert len(result.cards) == 2
