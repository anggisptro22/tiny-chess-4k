# Build task (agent instructions)

You are building a chess engine entry for the make.fun bounty tiny-chess-01 in this repository.

## The deliverable
`main.py` at the repository root: a chess engine in **at most 4,096 bytes** (bytes of the committed file, comments included). Constraints from the competition rules:

- Python 3.13, standard library only. No third-party imports, no other files read at trial time (the engine may not read anything but its own bytes and the brief).
- It is driven by the trial env over HTTP: it POSTs to the routes described in the brief (`/game`, `/move`, `/resign`), using `urllib.request` from the stdlib. The brief's path is in env var MAKEFUN_PROMPT_FILE; the env origin in MAKEFUN_ENV_URL. When those variables are missing (local testing), default to http://127.0.0.1:8080 and a brief file path you pass in.
- Determinism: every move must come from the position and history only. NO wall-clock use inside the search, no unseeded randomness. Keep a fixed per-move node budget so a move takes well under the 10,000 ms limit (the trial runs on 1 CPU, ~2-3 s per move average; aim for ~2 s per move locally).
- All 8 games of a trial must be played in one process run; loop until the env answers {"status": "done"} to POST /game.

## Engine design guidance
- Board: a 10x12 (120-square) mailbox or 0x88 representation is compact and fast in Python.
- Search: iterative deepening alpha-beta with a fixed node budget per move, capture/promotion + check-evasion extensions, transposition table keyed by position hash, killer-move ordering.
- Evaluation: material (pawn 100, knight 320, bishop 330, rook 500, queen 900) plus piece-square tables and bishop pair, similar spirit to the house engines (they evaluate exactly that).
- Keep the source readable first (README-sized working version), then MINIMIZE to under 4,096 bytes at the very end while keeping identical behaviour. Verify the byte count and that it still plays correctly after minifying.

## Rules for you
- Write all code yourself; do not copy any existing open-source engine file (no sunfish code — it is GPL and copying it verbatim would break the entry). Deriving from a written description is fine.
- Test your work: run the kit's local grader from /workspace/makefun/tiny-chess-01-kit with `node cli/makefun.mjs grade-local --kit . --bot /workspace/makefun/chess-bot --driver process --instances 1` and iterate until the practice Elo is as high as you can get it.
- The repository must stay tiny: main.py, LICENSE, README.md only (whole snapshot under 8,192 bytes total; no file over 4,096). Keep README.md under 2 KB.
- Do not git-commit; leave that to the operator.
