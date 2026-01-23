from typing import List, Literal
from pydantic import BaseModel, field_validator

class DAGNode(BaseModel):
    id: str
    role: Literal["worker", "reflector", "validator"]
    task: str
    deps: List[str]

    @field_validator("id")
    @classmethod
    def id_must_not_be_empty(cls, v: str):
        if not v.strip():
            raise ValueError("id must be non-empty")
        return v
