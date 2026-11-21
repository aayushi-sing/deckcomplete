import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { analyzeCollection } from "./api";

const sample = {
  unrecognized_lines: [
    { line_number: 2, text: "???", reason: "Unsupported line" },
  ],
  matches: [
    {
      deck_name: "Sample",
      owned_cards: 1,
      total_cards: 2,
      percent_owned: 50,
      missing: [{ name: "Pikachu", needed: 2, owned: 1 }],
    },
  ],
};

const fetchMock = vi.fn<typeof fetch>();

beforeEach(() => {
  vi.stubEnv("NEXT_PUBLIC_API_URL", undefined);
  vi.stubGlobal("fetch", fetchMock);
  fetchMock.mockReset();
  fetchMock.mockImplementation(() => Promise.resolve(Response.json(sample)));
});

afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
});

describe("analyzeCollection", () => {
  it("returns the parsed successful response", async () => {
    await expect(analyzeCollection("1 Pikachu")).resolves.toEqual(sample);
  });

  it("posts the exact text as JSON", async () => {
    const text = "  1 Pikachu\n???  ";
    await analyzeCollection(text);
    expect(fetchMock).toHaveBeenCalledExactlyOnceWith(
      "http://127.0.0.1:8000/match",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      },
    );
  });

  it("uses the default URL for absent and empty environment values", async () => {
    await analyzeCollection("");
    vi.stubEnv("NEXT_PUBLIC_API_URL", "");
    await analyzeCollection("");
    expect(fetchMock).toHaveBeenCalledTimes(2);
    for (const [url] of fetchMock.mock.calls) {
      expect(url).toBe("http://127.0.0.1:8000/match");
    }
  });

  it("reads the URL on each call and removes trailing slashes", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://api.example.test///");
    await analyzeCollection("");
    expect(fetchMock.mock.calls[0][0]).toBe("https://api.example.test/match");
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://other.example.test");
    await analyzeCollection("");
    expect(fetchMock.mock.calls[1][0]).toBe("https://other.example.test/match");
  });

  it("throws a clear status-based error for non-2xx responses", async () => {
    for (const status of [422, 500]) {
      fetchMock.mockResolvedValueOnce(new Response(null, { status }));
      await expect(analyzeCollection("")).rejects.toThrow(
        `Collection analysis failed (HTTP ${status})`,
      );
    }
  });

  it("propagates the original network error", async () => {
    const error = new TypeError("Network unavailable");
    fetchMock.mockRejectedValueOnce(error);
    await expect(analyzeCollection("")).rejects.toBe(error);
  });

  it("propagates the original JSON parsing error", async () => {
    const error = new SyntaxError("Invalid JSON");
    const response = new Response("invalid");
    vi.spyOn(response, "json").mockRejectedValueOnce(error);
    fetchMock.mockResolvedValueOnce(response);
    await expect(analyzeCollection("")).rejects.toBe(error);
  });
});
