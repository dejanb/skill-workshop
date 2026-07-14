"""Utility functions."""


def format_name(first: str, last: str) -> str:
    return f"{first.strip()} {last.strip()}"


def parse_csv_line(line: str) -> list[str]:
    return [field.strip() for field in line.split(",")]
