from app.core.parser import parse_line


def test_parses_quantity_name_set_and_number():
    result = parse_line("4 Professor's Research SVI 189")
    assert result is not None
    assert result.quantity == 4
    assert result.name == "Professor's Research"
    assert result.set_code == "SVI"
    assert result.number == "189"


def test_parses_name_with_ex_suffix():
    result = parse_line("3 Charizard ex OBF 125")
    assert result is not None
    assert result.quantity == 3
    assert result.name == "Charizard ex"
    assert result.set_code == "OBF"
    assert result.number == "125"


def test_parses_line_without_set_info():
    result = parse_line("2 Pikachu")
    assert result is not None
    assert result.quantity == 2
    assert result.name == "Pikachu"
    assert result.set_code is None
    assert result.number is None


def test_lines_without_a_quantity_return_none():
    assert parse_line("Pokémon: 12") is None
    assert parse_line("") is None


def test_header_without_accent_returns_none():
    assert parse_line("Pokemon: 12") is None


def test_x_after_quantity_is_not_supported():
    assert parse_line("4x Pikachu") is None


def test_leading_zero_quantity_returns_none():
    assert parse_line("04 Pikachu") is None


def test_incomplete_metadata_becomes_part_of_the_name():
    result = parse_line("2 Pikachu SVI")
    assert result is not None
    assert result.name == "Pikachu SVI"
    assert result.set_code is None
    assert result.number is None


def test_leading_zeros_in_card_number_are_preserved():
    result = parse_line("1 Pikachu SVI 007")
    assert result is not None
    assert result.number == "007"


def test_tab_between_quantity_and_name_is_accepted():
    result = parse_line("3\tPikachu")
    assert result is not None
    assert result.quantity == 3
    assert result.name == "Pikachu"
