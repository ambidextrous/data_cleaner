from dataclasses import dataclass


@dataclass
class MaterialAttribute:
    name: str
    value_range: tuple
    temperature: int = None
