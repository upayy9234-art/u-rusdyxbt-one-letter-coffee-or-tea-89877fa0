#!/usr/bin/env python3
"""One Letter: Coffee or Tea — pick the single letter that wins the argument.

The bounty asks for exactly one letter and nothing else: A for coffee, B
for tea. A judge model reads two letters at a time and picks the one whose
choice of coffee or tea feels more vivid, funnier or truer. The gate is
strict: /output/entry.txt must hold exactly one character, A or B, no word,
no explanation, no punctuation, no trailing newline. Only a valid entry
goes before the judge; an invalid one is listed with 0 and takes no prize.

So the whole entry is a choice between two drinks, and the program makes
that choice the way the judge's brief says to weigh it, most important
first:

  1. vivid   — the choice lands as a fuller, more alive answer for the
               drink it names
  2. funny   — the choice carries more wit or surprise for the drink
  3. true    — the choice stands as the more honest answer for the
               person who sends it
  4. stands  — the letter stands on its own as a whole answer, clean
               and unmistakable, with nothing needed beside it

Each drink is scored 0-10 on those four, weighted 3/2/2/1 in the brief's
own order. The scores below are judgements about the drink, not the
letter, and every score carries its reason in the table so the choice can
be checked, not just trusted.

Why coffee wins here, in one paragraph: coffee is the louder drink. It
announces itself — the smell fills the room before the cup reaches you,
the first sip is a jolt you feel in your chest, dark and steaming and
bitter. It is the drink with the jokes attached ("don't talk to me
before coffee", the third refill, espresso yourself, depresso), because
the need for it is a joke everybody recognises. And it is the honest
answer for a person about to do a long day's work: the morning lifeline
of every office, the default "let's grab a coffee", the first letter of
the alphabet for the first drink of the day. Tea is a fine drink — the
most drunk on earth after water, ancient, calm, honest in a quiet way —
but quiet is exactly what loses on vivid and funny, and the brief weighs
those two first. Tea's ceremony is beautiful and its puns ("spill the
tea") are real, but the drink itself is earnest where coffee is alive.

The program is fully deterministic: no randomness, no clock, no network,
no input, no environment read except the output directory. Pure Python
standard library only.
"""

import os

# Weights follow the judge's brief: vivid first, then funny, then true,
# then how well the letter stands on its own as a whole answer.
WEIGHT_VIVID = 3
WEIGHT_FUNNY = 2
WEIGHT_TRUE = 2
WEIGHT_STANDS = 1

# The two drinks the bounty offers, in the order the bounty names them.
# A is coffee, B is tea. Nothing else is a legal entry: the gate accepts
# exactly one character, and the judge's first criterion says anything
# else loses to any letter that chooses coffee or tea.
LETTER_COFFEE = "A"
LETTER_TEA = "B"


class Drink:
    """One of the two choices: its letter, its drink, and its scores.

    Each score is a judgement about the drink on one of the judge's
    criteria, 0 to 10, with the reason written next to it in the table
    below so the numbers are not bare assertions.
    """

    def __init__(self, letter, drink, vivid, funny, true, stands,
                 reasons):
        self.letter = letter
        self.drink = drink
        self.vivid = vivid
        self.funny = funny
        self.true = true
        self.stands = stands
        self.reasons = reasons

    def base_score(self):
        """Weighted sum in the brief's order of importance."""
        return (
            WEIGHT_VIVID * self.vivid
            + WEIGHT_FUNNY * self.funny
            + WEIGHT_TRUE * self.true
            + WEIGHT_STANDS * self.stands
        )

    def total(self):
        return self.base_score()

    def report(self):
        """One line per drink: the scores and the weighted total."""
        return (
            "%s for %-6s vivid %2d funny %2d true %2d stands %2d "
            "total %2d"
            % (
                self.letter,
                self.drink,
                self.vivid,
                self.funny,
                self.true,
                self.stands,
                self.total(),
            )
        )

    def reasons_report(self):
        """The reasons behind the scores, one line per criterion."""
        lines = ["%s for %s:" % (self.letter, self.drink)]
        for name in ("vivid", "funny", "true", "stands"):
            lines.append(
                "  %-6s %2d/10 — %s"
                % (name, getattr(self, name), self.reasons[name])
            )
        return "\n".join(lines)


def build_drinks():
    """The two choices, scored against the judge's brief.

    Coffee first, because the bounty names it first and because the
    alphabet does: A is the first letter for the first drink of the day.
    """
    return [
        Drink(
            LETTER_COFFEE,
            "coffee",
            # Vivid: the smell fills the room before the cup reaches
            # you; dark, steaming, bitter; the first sip is a jolt you
            # feel in your chest. No other everyday drink announces
            # itself that loudly.
            vivid=9,
            # Funny: the jokes are attached to the need itself —
            # "don't talk to me before coffee", the third refill,
            # "espresso yourself", "depresso". Everybody recognises
            # the dependency, so the joke lands at once.
            funny=9,
            # True: the morning lifeline of every office, the default
            # "let's grab a coffee", the drink people reach for when
            # there is a long day to get through. An honest answer
            # for the person sending it.
            true=9,
            # Stands: A is the first letter of the alphabet, and
            # coffee is the first drink of the day. The letter needs
            # nothing beside it to be understood.
            stands=9,
            reasons={
                "vivid": (
                    "the smell fills the room, dark and steaming, "
                    "the first sip a jolt you feel in your chest"
                ),
                "funny": (
                    "\"don't talk to me before coffee\", the third "
                    "refill, \"espresso yourself\" — the jokes ride "
                    "on a need everybody recognises"
                ),
                "true": (
                    "the morning lifeline of every office, the "
                    "default \"let's grab a coffee\" before a long day"
                ),
                "stands": (
                    "A is the first letter, coffee the first drink "
                    "of the day — nothing else is needed beside it"
                ),
            },
        ),
        Drink(
            LETTER_TEA,
            "tea",
            # Vivid: gentle steam, pale gold, a quiet cup. Beautiful,
            # but quiet — it does not fill a room the way coffee does.
            vivid=7,
            # Funny: "spill the tea" is a real joke, and tea has its
            # puns, but the drink itself is earnest; the humour is
            # about gossip, not about the cup.
            funny=6,
            # True: the most drunk drink on earth after water, ancient
            # and honest, the calm cup at the end of a long day. Very
            # true — just quieter about it than coffee.
            true=8,
            # Stands: B is the second letter for the second cup, the
            # calmer choice. Clear on its own, but it reads as the
            # alternative rather than the default.
            stands=8,
            reasons={
                "vivid": (
                    "gentle steam and pale gold — beautiful, but "
                    "quiet; it never fills a room the way coffee does"
                ),
                "funny": (
                    "\"spill the tea\" is real, but the joke is about "
                    "gossip, not the cup; the drink itself is earnest"
                ),
                "true": (
                    "the most drunk drink on earth after water, "
                    "ancient and honest, the calm cup at day's end"
                ),
                "stands": (
                    "B is the second letter for the second cup — "
                    "clear alone, but it reads as the alternative"
                ),
            },
        ),
    ]


def pick_winner(drinks):
    """Highest total wins; ties break to the earlier letter, so the pick
    is stable and the same on every run.

    The tie-break is explicit in the sort key, not left to the order the
    table happens to list the drinks in: a drink wins on its total, and
    only when totals are equal does the earlier letter win.
    """
    return max(drinks, key=lambda d: (d.total(), -ord(d.letter)))


def verify_order_independence(drinks):
    """Prove the pick does not depend on the table's order: score the
    same drinks in reverse and require the same winner. A pick that
    moved with the listing order would be an artefact of the table,
    not a judgement about the drinks."""
    forward = pick_winner(drinks)
    backward = pick_winner(list(reversed(drinks)))
    assert forward.letter == backward.letter, (
        "winner changes with table order: %s vs %s"
        % (forward.letter, backward.letter)
    )
    return forward


def validate(drinks):
    """Sanity checks on the table itself, before anything is written."""
    letters = [d.letter for d in drinks]
    assert len(drinks) == 2, "the table must hold exactly two drinks"
    assert sorted(letters) == [LETTER_COFFEE, LETTER_TEA], (
        "the table must hold A for coffee and B for tea, exactly once each"
    )
    for drink in drinks:
        for name in ("vivid", "funny", "true", "stands"):
            value = getattr(drink, name)
            assert 0 <= value <= 10, "%s score out of range for %s" % (
                name,
                drink.letter,
            )
        assert drink.total() >= 0, "negative total for %s" % drink.letter
        assert set(drink.reasons) == {"vivid", "funny", "true", "stands"}, (
            "every criterion needs its reason for %s" % drink.letter
        )


def write_entry(letter, output_dir):
    """Write exactly one character to entry.txt, no trailing newline.

    The gate allows exactly one character, A or B, and nothing else:
    no word, no gloss, no punctuation, no trailing newline. The file
    is read back and checked before the program reports success, so a
    bad write fails loudly here instead of silently at the gate.
    """
    assert len(letter) == 1 and letter in (LETTER_COFFEE, LETTER_TEA), (
        "entry must be exactly one letter, A or B, got %r" % letter
    )
    os.makedirs(output_dir, exist_ok=True)
    entry_path = os.path.join(output_dir, "entry.txt")
    with open(entry_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(letter)
    with open(entry_path, "rb") as handle:
        written = handle.read()
    assert written == letter.encode("ascii"), (
        "entry.txt holds %r, not the single letter %r"
        % (written, letter)
    )
    assert len(written) == 1, "entry.txt must be exactly 1 byte"
    return entry_path


def main():
    drinks = build_drinks()
    validate(drinks)

    # The pick must not depend on the order the table lists the drinks
    # in; verify that before anything is written.
    winner = verify_order_independence(drinks)

    for drink in drinks:
        print(drink.reasons_report())
        print(drink.report())
    print(
        "winner: %s for %s (total %d)"
        % (winner.letter, winner.drink, winner.total())
    )

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    entry_path = write_entry(winner.letter, output_dir)
    print("wrote %s" % entry_path)


if __name__ == "__main__":
    main()
