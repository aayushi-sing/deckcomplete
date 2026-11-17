# AGENTS.md — DeckComplete

Rules for any AI coding agent working in this repo. Read this before every task.

## What this project is

DeckComplete is a web tool for Pokémon TCG players. A player pastes the cards
they own, picks a format, and sees which known decks they can build or nearly
build, with the percentage owned and the missing cards listed.

It is an unofficial fan project, not affiliated with Nintendo, Game Freak or
The Pokémon Company. Card images come from the API's image links; never copy
images into this repo.

The owner is new to building a project this large. Explain terms briefly, say
what to check after each step, and never make large changes silently.

## Architecture (do not change without asking)

Browser (Next.js) -> FastAPI backend -> core engine (plain Python) -> data files.

- `backend/app/core/` holds the engine: `parser.py`, `validator.py`,
  `matcher.py`, `models.py`. These are plain functions and Pydantic models.
  They must NOT import FastAPI or do any network or file I/O inside the logic.
- `backend/app/main.py` is a thin FastAPI layer. It validates requests,
  calls the engine and returns JSON. No business logic here.
- `backend/app/data/` holds `cards.json` and `decklists/*.json`.
- `backend/scripts/fetch_cards.py` downloads card data once from pokemontcg.io.
  The app must never call that API per user request.
- `frontend/` is Next.js + TypeScript + Tailwind.
- `backend/tests/` mirrors `backend/app/core/`.
- `backend/app/ai/` (created later) holds ALL LLM and vision code. See
  "AI integration" below.

## Stack

Python, FastAPI, Pydantic, pytest, RapidFuzz. Next.js, TypeScript, Tailwind.
JSON or SQLite for now. Postgres comes later, only when the owner asks.
Do not add a new library without asking first and saying why it is needed.
Check that a library and function exist in its real docs before using them.

## Commands (update these once the project exists)

Run the backend commands from the `backend` folder.

- Backend tests: `.\.venv\Scripts\python.exe -m pytest`
- Run backend: `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload`
- Run frontend: `cd frontend && npm run dev`
- Fetch card data: `.\.venv\Scripts\python.exe scripts/fetch_cards.py`

## How to work

1. One small task at a time (one file or one feature). Do not do extra work.
2. Write tests first, then the code that makes them pass.
3. Never change or delete a test just to make it pass. If a test looks wrong,
   stop and explain why.
4. Before finishing, run the tests and report what passed and failed.
5. Show what you changed and why. Keep diffs small and targeted; do not
   rewrite whole files unless asked.
6. Use a git branch per task and small commits with clear messages.
7. Before any task that involves a design choice (a data shape, a library, how
   to handle an edge case), propose the options with trade-offs and a
   recommendation, then wait for the owner's approval. Do not decide silently.
   This takes priority over doing the work quickly.
8. If you think the plan or an instruction is wrong or risky, say so before
   implementing, and explain why in beginner-friendly terms.
9. Before changing files, say what you intend to change. Afterward, summarize
   what changed, why, which tests ran and their results.
10. Check unfamiliar libraries, APIs, Pokémon TCG rules and data formats
    against real documentation. If you could not verify something, say so.

## Domain rules (verify, do not guess)

- A deck has exactly 60 cards.
- At most 4 copies of cards with the same name, except basic energy.
- At least 1 Basic Pokémon.
- Standard legality is decided by regulation marks. Keep the list of legal
  marks in one data file with a source link and date. Never hard-code
  rotation from memory, and do not rely only on the API's legality field.
- Match cards by name first (printings are usually interchangeable). Treat
  same-name cards with different effects as a known edge case to handle later.
- Every hand-entered decklist must be checked for legality by the owner.
  Check a source site's terms before copying its decklists.
- The parser must flag unrecognized lines. It must never silently drop them.

## AI integration (only after the core engine works and the owner asks)

AI lives at the edges of the app. The rules engine stays deterministic.

- All LLM and vision code goes in `backend/app/ai/`. Nothing in
  `backend/app/core/` may import from `backend/app/ai/`. The app must still
  work with AI turned off.
- An LLM never builds a deck on its own and never decides legality. Every AI
  output (parsed cards, extracted constraints, suggested substitutions) is
  checked by the validator before the user sees it.
- Allowed uses, in this order: (1) explanations written from the matcher's
  structured result plus real card text from our data, (2) turning a
  plain-English request into constraints validated by Pydantic, (3) card
  substitutions checked by the validator, (4) photo import, which outputs text
  lines that go through the normal parser and a user-editable preview.
- The LLM only gets structured data and card text from our database. It must
  not rely on memory for card abilities. Check that every card it mentions is
  actually in the deck.
- Show the user what the AI read or suggested and let them correct it.
- Cache AI results and rate-limit requests. Keep API keys in `.env`.
- Every AI feature needs a measurable test (for example, the share of
  suggestions that pass the validator, or accuracy on a photo test set).
- Call things what they are: OR-Tools budget completion is optimization, not
  machine learning. Do not describe features as AI in the README unless an AI
  model actually does the work.

## Security and data

- The Pokémon TCG API key lives in `.env` (listed in `.gitignore`). Never
  commit it, print it or put it in code.
- No user accounts, saved data or analytics unless the owner asks.

## Not in scope for now (do not build)

Card scanning, store widget or checkout, live prices, accounts, LangGraph or
other agent frameworks, and MCP. LLM and vision features wait until the core
engine works and the owner asks (see "AI integration"). Budget optimization
with OR-Tools comes later and only on request.

## Honesty

Do not claim a feature works until a test or a manual run shows it does.
If you are unsure, say so. Do not describe planned features as built in the
README, comments or commit messages.