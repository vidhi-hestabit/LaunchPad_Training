import os
import sys
sys.path.append(os.path.abspath("."))
from day_4.src.generator.llm_client import get_openai_client
from day_4.src.utils.schema_loader import load_schema
from day_4.src.utils.db_executor import execute_sql


def print_table(columns, rows):
    print("\nRESULT TABLE:\n")
    print(" | ".join(columns))
    print("-" * 80)

    for row in rows:
        print(" | ".join(map(str, row)))

    print(f"\nTotal rows: {len(rows)}")



def generate_sql(question: str, schema: str) -> str:
    client = get_openai_client()

    prompt = f"""
You are a SQL expert.

Given the database schema:
{schema}

Write a SINGLE valid SQL query that answers:
"{question}"

Rules:
- Use only **one table at a time**
- Do NOT use joins or UNIONs
- Do NOT perform any DELETE operation
- Use only tables and columns from the schema
- Do NOT explain
- Do NOT use backticks
- Return SQL only
"""


    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    db_path = "day_4/src/data/employee.db"

    print("\nSQL Generator Test\n")
    question = input("Enter your question:\n> ")

    schema = load_schema(db_path)

    sql = generate_sql(question, schema)
    print("Generated SQL:\n", sql)
    # 4. Execute SQL
    columns, rows = execute_sql(db_path, sql)

    # 5. Print result table
    print_table(columns, rows)

    print(sql)
