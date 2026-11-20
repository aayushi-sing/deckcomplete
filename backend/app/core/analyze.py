from app.core.matcher import build_collection, match_all
from app.core.models import AnalysisResult, Decklist
from app.core.parser import parse_list


def analyze(text: str, decklists: list[Decklist]) -> AnalysisResult:
    parsed = parse_list(text)
    collection = build_collection(parsed.cards)
    return AnalysisResult(
        unrecognized_lines=parsed.unrecognized_lines,
        matches=match_all(collection, decklists),
    )
