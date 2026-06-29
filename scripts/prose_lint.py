#!/usr/bin/env python3
"""Prose readability linter for DACS normative spec text (SPEC-STYLE.md).

Flags, in prose paragraphs of spec markdown:

- long-sentence   : sentence > --max-sentence-words (default 35) words
- long-paragraph  : non-list prose paragraph > --max-paragraph-words (default 100) words
- parentheticals  : sentence with more than one parenthetical group
- keyword-density : non-list prose paragraph with > 2 RFC 2119 keyword obligations
                    (rule *bullets* are exempt: one bullet = one rule)

Skips code fences, tables, and headings. Blockquote `> **Note (non-normative).**` blocks
are exempt from sentence-level checks but still subject to the paragraph cap.

Waiver: an HTML comment line `<!-- prose-lint: allow ... -->` immediately before a
paragraph suppresses its findings (counted and reported).

Exit code 1 when violations are found (waived findings do not fail the run).
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

RFC_KEYWORD_RE = re.compile(
    r"\b(MUST NOT|MUST|SHALL NOT|SHALL|SHOULD NOT|SHOULD|REQUIRED|RECOMMENDED|OPTIONAL|MAY)\b"
)
WAIVER_RE = re.compile(r"<!--\s*prose-lint:\s*allow\b")
# Abbreviations that end with '.' but do not end a sentence.
ABBREV_RE = re.compile(r"\b(e\.g|i\.e|cf|vs|etc|v0|v1|v2|No|§\S*)\.$")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=\S)")


@dataclass
class Finding:
    path: str
    line: int
    kind: str
    measure: str
    excerpt: str
    waived: bool

    def render(self) -> str:
        flag = " [waived]" if self.waived else ""
        return f"{self.path}:{self.line}: {self.kind} ({self.measure}){flag}\n    {self.excerpt}"


def strip_markup(text: str) -> str:
    text = re.sub(r"`[^`]*`", "CODE", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return text.replace("**", "").replace("*", "")


def split_sentences(text: str) -> list[str]:
    parts: list[str] = []
    for raw in SENTENCE_SPLIT_RE.split(text):
        raw = raw.strip()
        if not raw:
            continue
        if parts and ABBREV_RE.search(parts[-1]):
            parts[-1] = parts[-1] + " " + raw
        else:
            parts.append(raw)
    return parts


def word_count(text: str) -> int:
    return len(strip_markup(text).split())


def paren_groups(sentence: str) -> int:
    # Ignore rule-ID anchors like (PC-2) / (RAV-R4), bare cross-refs like (§9.4.4),
    # enumeration anchors like (a) / (ii) / (#27), and parens whose content is
    # entirely inline code (already collapsed to CODE).
    cleaned = re.sub(r"\((?:[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-?\d+|§[^)]*|[a-z]|i{1,3}v?|#\d+)\)", "", sentence)
    cleaned = re.sub(r"\((?:CODE|[\s,/]|or CODE)*\)", "", cleaned)
    return cleaned.count("(")


@dataclass
class Para:
    line: int
    text: str
    is_list_item: bool
    is_note: bool
    waived: bool


def parse_paragraphs(lines: list[str]) -> list[Para]:
    paras: list[Para] = []
    in_code = False
    buf: list[str] = []
    buf_line = 0
    buf_list = False
    buf_note = False
    pending_waiver = False

    def flush() -> None:
        nonlocal buf, pending_waiver
        if buf:
            paras.append(Para(buf_line, " ".join(buf), buf_list, buf_note, pending_waiver))
            pending_waiver = False
        buf = []

    for i, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush()
            in_code = not in_code
            continue
        if in_code:
            continue
        if WAIVER_RE.search(stripped):
            flush()
            pending_waiver = True
            continue
        if not stripped:
            flush()
            continue
        # Indented code blocks (4+ spaces / tab at paragraph start).
        if not buf and re.match(r"^(?: {4,}|\t)", line):
            continue
        if stripped.startswith("#") or stripped.startswith("|") or set(stripped) <= {"-", " "}:
            flush()
            continue
        is_note = stripped.startswith(">")
        body = re.sub(r"^>\s?", "", stripped) if is_note else stripped
        if is_note and not body:
            # `>` blank line: paragraph break inside a blockquote.
            flush()
            continue
        if is_note and body.startswith("|"):
            flush()
            continue
        is_list = bool(re.match(r"^\s*(?:[-*+]|\d+\.)\s+", body))
        if is_list:
            flush()
            buf = [re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", body)]
            buf_line, buf_list, buf_note = i, True, is_note
            flush()
        else:
            if not buf:
                buf_line, buf_list, buf_note = i, False, is_note
            buf.append(body)
    flush()
    return paras


def lint_file(path: Path, max_sentence: int, max_paragraph: int) -> list[Finding]:
    findings: list[Finding] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    rel = str(path)
    # Lazy-continuation hazard: a non-blank, non-quote line directly after a
    # blockquote is absorbed INTO the blockquote when rendered — normative text
    # ends up displayed inside a non-normative Note.
    for i in range(1, len(lines)):
        prev, cur = lines[i - 1].strip(), lines[i].strip()
        if prev.startswith(">") and cur and not cur.startswith(">"):
            findings.append(
                Finding(rel, i + 1, "note-continuation", "missing blank line after blockquote",
                        cur[:90] + "…", False)
            )
    for p in parse_paragraphs(lines):
        wc = word_count(p.text)
        if not p.is_list_item and wc > max_paragraph:
            findings.append(
                Finding(rel, p.line, "long-paragraph", f"{wc} words", p.text[:90] + "…", p.waived)
            )
        if p.is_note:
            continue  # notes exempt from sentence-level checks
        for s in split_sentences(p.text):
            swc = word_count(s)
            if swc > max_sentence:
                findings.append(
                    Finding(rel, p.line, "long-sentence", f"{swc} words", s[:90] + "…", p.waived)
                )
            if paren_groups(s) > 1:
                findings.append(
                    Finding(rel, p.line, "parentheticals", f"{paren_groups(s)} groups", s[:90] + "…", p.waived)
                )
        if not p.is_list_item:
            kw = len(RFC_KEYWORD_RE.findall(p.text)) - len(
                re.findall(r"\b(?:MUST|SHALL|SHOULD) NOT\b", p.text)
            )
            if kw > 2:
                findings.append(
                    Finding(rel, p.line, "keyword-density", f"{kw} keywords", p.text[:90] + "…", p.waived)
                )
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--max-sentence-words", type=int, default=35)
    ap.add_argument("--max-paragraph-words", type=int, default=100)
    ap.add_argument("--summary", action="store_true", help="print counts only")
    args = ap.parse_args()

    all_findings: list[Finding] = []
    for path in args.paths:
        all_findings.extend(lint_file(path, args.max_sentence_words, args.max_paragraph_words))

    active = [f for f in all_findings if not f.waived]
    waived = [f for f in all_findings if f.waived]
    if not args.summary:
        for f in all_findings:
            print(f.render())
    by_kind: dict[str, int] = {}
    for f in active:
        by_kind[f.kind] = by_kind.get(f.kind, 0) + 1
    summary = ", ".join(f"{k}: {v}" for k, v in sorted(by_kind.items())) or "clean"
    print(f"\nprose-lint: {len(active)} active ({summary}); {len(waived)} waived")
    return 1 if active else 0


if __name__ == "__main__":
    sys.exit(main())
