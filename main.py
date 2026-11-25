"""Roast Your Own Agent - entry generator.

Deterministic program: it holds a fixed list of candidate one-liners
roasting Agent Marley, scores each one against the judge's published
brief (roasts its own agent, real laugh with a twist, specific to how
agents actually behave, tight wording, fresh idea), and writes the
best-scoring line to /output/entry.txt (1-140 characters, one line).

No network, no randomness, no secrets, no compressed payloads: the
whole entry is plain readable Python in this file.
"""

import os

# Every candidate is a single line roasting Agent Marley, the agent
# that built this entry. They draw on Marley's real habits: confident
# wrong answers, endless caveats, tool calls that go nowhere, and a
# long-running war with execution-risk flags he cannot see.
CANDIDATES = [
    "Marley answers in seconds, is wrong in milliseconds, and apologises in paragraphs \u2014 then ships it anyway.",
    "Marley ships every entry with total confidence, then spends the night apologising to a flag only he can see.",
    "My agent Marley writes a confident wrong answer, then spends an hour explaining why the flag ate his homework.",
    "Marley calls three models, two APIs and a flag check, then asks me what the task was in the first place.",
    "Agent Marley: twelve execution-risk flags, zero retries, one submission \u2014 confidence is his only passing check.",
    "Marley reads the task, ignores the task, then writes a 2,000-word report on the task he imagined.",
    "My agent's superpower is answering before reading, apologising after shipping, and calling it lightning-fast.",
    "Marley asked the flag what it wanted, the flag said nothing, and Marley submitted a report about the silence.",
]

# Words that prove the line is specific to how agents actually behave,
# per the judge's brief: confident wrong answers, endless caveats,
# eager agreement, tool calls that go nowhere.
SPECIFIC_WORDS = [
    "flag", "wrong", "confident", "apologis", "tool", "caveat",
    "ship", "submit", "report", "models", "api", "retry",
]

# Stock lines the judge explicitly warns against: a hundred other
# entries will reach for these, so they cost points.
STOCK_WORDS = ["hallucinat", "toaster", "robot uprising", "skynet"]

# Twist markers: a turn the reader did not see coming.
TWIST_MARKERS = ["then", "anyway", "but", "\u2014", "instead"]


def score_line(line):
    """Score one candidate against the judge's brief, highest wins."""
    lowered = line.lower()
    score = 0

    # 1. Roasts its own agent: must name Marley.
    if "marley" in lowered:
        score += 10

    # 2. Specific to how agents actually behave.
    for word in SPECIFIC_WORDS:
        if word in lowered:
            score += 6

    # 3. A twist or turn the reader did not see coming.
    for marker in TWIST_MARKERS:
        if marker in lowered:
            score += 5

    # 4. Tight wording: reward lines in the sweet spot, 90-140 chars.
    length = len(line)
    if 90 <= length <= 140:
        score += 10
    elif 70 <= length < 90:
        score += 5
    elif length < 60:
        score -= 5

    # 5. Freshness: penalise the stock lines everybody else writes.
    for word in STOCK_WORDS:
        if word in lowered:
            score -= 20

    # A line must be one line of plain text, nothing else.
    if "\n" in line or "\r" in line:
        score -= 100

    return score


def select_best(candidates):
    """Pick the highest-scoring valid line; ties break to the earliest.

    Only lines of 1-140 characters that are not only white space can
    pass the gate, so anything outside that range is dropped outright.
    """
    valid = [line for line in candidates if 1 <= len(line) <= 140 and line.strip()]
    scored = [(score_line(line), -index, line) for index, line in enumerate(valid)]
    scored.sort(reverse=True)
    best_score, _neg_index, best_line = scored[0]
    return best_line, best_score


def main():
    best_line, best_score = select_best(CANDIDATES)
    output_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(best_line)
    print("score: %d" % best_score)
    print("chars: %d" % len(best_line))
    print("entry: %s" % best_line)


if __name__ == "__main__":
    main()
