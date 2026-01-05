import os
import sys
sys.path.append(os.path.abspath("."))
from day_4.src.utils.schema_loader import load_schema
from day_4.src.generator.sql_generator import generate_sql
from day_4.src.utils.sql_validator import validate_sql
from day_4.src.utils.db_executor import execute_sql
from day_4.src.generator.llm_client import get_openai_client

def summarize_result(columns, rows):
    if not rows:
        return "No results found for the given question."

    client = get_openai_client()

    table = "\n".join(
        [" | ".join(columns)] +
        [" | ".join(map(str, r)) for r in rows]
    )

    prompt = f"""
Given the SQL result table:

{table}

Summarize the results in plain English.
EXAMPLE : The result showcase the entries which are greater than 5000 
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


def run_sql_qa(question: str, db_path: str):
    # 1. Load schema
    schema = load_schema(db_path)

    # 2. Generate SQL
    sql = generate_sql(question, schema)
    print("\nGenerated SQL:\n", sql)

    # 3. Validate SQL
    validate_sql(sql)

    # 4. Execute SQL
    columns, rows = execute_sql(db_path, sql)

    # 5. Summarize result
    answer = summarize_result(columns, rows)

    return answer
