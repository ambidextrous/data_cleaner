from typing import Dict, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True,eq=True)
class Material:
    name: str
    synonyms: tuple


class MaterialRetriever(ABC):
    @abstractmethod
    def contains_synonym(self, item: str) -> bool:
        pass

    @abstractmethod
    def get_by_synonym(self, item: str) -> Material:
        pass


class TestMaterialRetriever(MaterialRetriever):

    def __init__(self):
        self.synonym_dict = get_test_synonym_dict()

    def contains_synonym(self, synonym: str) -> bool:
        return synonym in self.synonym_dict

    def get_by_synonym(self, synonym: str) -> Material:
        return self.synonym_dict[synonym]


def get_test_synonym_dict() -> Dict[str, Material]:
    """
    Loads a minimal material dictionary for testing purpouses
    """
    zirconium_oxide = Material(
        name = 'Zirconium Oxide',
        synonyms=(
            'zirconium oxide',
            'zirconium dioxide', 
            'zirconia',
            'zro2',
            'o2zr'
        )
    )

    zirconium = Material(
        name='Zirconium',
        synonyms=('zirconium','zr')
    )

    copper = Material(
        name = 'Copper',
        synonyms=('copper','cu')
    )

    materials = [zirconium_oxide, zirconium, copper]

    synonym_dict = {}
    for material in materials:
        for synonym in material.synonyms:
            synonym_dict[synonym] = material

    return synonym_dict


