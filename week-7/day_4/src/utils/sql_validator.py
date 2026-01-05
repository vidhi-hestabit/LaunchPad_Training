import re

FORBIDDEN = ["drop", "delete", "insert", "update", "alter", "truncate"]

def validate_sql(sql: str):
    lowered = sql.lower()

    if not lowered.strip().startswith("select"):
        raise ValueError("Only SELECT queries allowed")

    for word in FORBIDDEN:
        if word in lowered:
            raise ValueError(f"Forbidden keyword detected: {word}")

    if ";" in lowered[:-1]:
        raise ValueError("Multiple SQL statements detected")

    if not re.search(r"\bfrom\b", lowered):
        raise ValueError("Invalid SQL syntax")
