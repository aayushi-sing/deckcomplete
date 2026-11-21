export interface UnrecognizedLine {
  line_number: number;
  text: string;
  reason: string;
}

export interface MissingCard {
  name: string;
  needed: number;
  owned: number;
}

export interface DeckMatch {
  deck_name: string;
  owned_cards: number;
  total_cards: number;
  percent_owned: number;
  missing: MissingCard[];
}

export interface AnalysisResult {
  unrecognized_lines: UnrecognizedLine[];
  matches: DeckMatch[];
}

export async function analyzeCollection(text: string): Promise<AnalysisResult> {
  const baseUrl = (
    process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
  ).replace(/\/+$/, "");
  const response = await fetch(`${baseUrl}/match`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    throw new Error(`Collection analysis failed (HTTP ${response.status})`);
  }

  return response.json();
}
