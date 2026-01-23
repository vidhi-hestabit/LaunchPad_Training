def extract_json_object(text: str):
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON object found")

    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]

    raise ValueError("Unbalanced JSON braces")
