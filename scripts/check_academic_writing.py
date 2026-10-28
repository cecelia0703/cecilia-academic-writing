#!/usr/bin/env python3
"""Heuristic style prompts, not an AI detector or grammar/citation validator.
Usage: python scripts/check_academic_writing.py paper.txt
"""
import pathlib
import re
import sys

PATTERNS = {
    'formulaic reversal': r'\bnot\s+only\b[\s\S]{0,180}?\bbut\s+also\b|\bnot\s+(?:merely|simply)\b[\s\S]{0,180}?\bbut\b',
    'generic filler': r'\bit is (?:important to note|worth mentioning) that\b|\bin today.s rapidly (?:changing|evolving) world\b',
    'inflated significance': r'\bthis (?:highlights|underscores) the crucial importance of\b|\bthe significance of .*? cannot be overstated\b',
    'enumerated transition': r'\b(?:firstly|secondly|thirdly|furthermore|moreover|additionally)\s*,',
}

def main(path):
    text = pathlib.Path(path).read_text(encoding='utf-8')
    flagged = 0
    for label, pattern in PATTERNS.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            line = text.count('\n', 0, match.start()) + 1
            snippet = ' '.join(match.group(0).split())[:130]
            print(f'{path}:{line}: {label}: {snippet}')
            flagged += 1
    print(f'Heuristic flags: {flagged}. Review in context; none proves AI authorship.')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python check_academic_writing.py FILE.txt')
    main(sys.argv[1])
