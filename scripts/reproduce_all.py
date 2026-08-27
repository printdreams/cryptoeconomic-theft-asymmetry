#!/usr/bin/env python3
"""Regenerate the complete set of committed equation outputs."""

from theft_asymmetry.runner import run_all


if __name__ == "__main__":
    for output in run_all():
        print(output)

