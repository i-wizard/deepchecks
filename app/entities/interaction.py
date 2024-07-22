from dataclasses import dataclass
from typing import Optional
from typing import TypedDict

from app.entities import BaseEntity


@dataclass
class InteractionEntity(BaseEntity):
    identifier: int
    input: str
    output: str

    @classmethod
    def get_collection(cls):
        return "interaction"

    def to_dict(self):
        return {
            "identifier": self.identifier,
            "input": self.input,
            "output": self.output
        }
