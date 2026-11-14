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
