#!/usr/bin/env python3
"""Run any manuscript equation by number."""

from __future__ import annotations

import argparse
from pathlib import Path

from theft_asymmetry.runner import run_equation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int, choices=range(1, 22))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    print(run_equation(args.number, args.output))


if __name__ == "__main__":
    main()

