import re
import string
from typing import Callable

from data_cleaner_app.normalizers.helpers import get_temperature, get_value_range, get_initial_numeric_value
from data_cleaner_app.data_classes import NumericMaterial

DENSITY_CONVERSION = {
    "gc": lambda x: x,
    "gcc": lambda x: x,
    "kgm": lambda x: x * 0.001,
    "kgmc": lambda x: x * 0.001,
    "kgl": lambda x: x,
    "gml": lambda x: x,
    "tm": lambda x: x,
    "tmc": lambda x: x,
}


def get_density(density: str) -> str:
    # If zero value given, assume units correct and return
    if density == "0":
        return "0"

    # If no density value provided, return empty string
    if not density:
        return ""

    material = NumericMaterial(
        single_value=get_initial_numeric_value(density),
        value_range=get_value_range(density),
        temperature=get_temperature(density),
        conversion=get_density_unit_convertion_function(density)
    )

    return material.format() 


def get_density_unit_convertion_function(given_density: str) -> Callable[[float],float]:

    # Strip non unit characters from density
    characters_to_remove = set(string.digits).union(set(string.punctuation))

    stripped_density = ""
    for char in given_density:
        if char not in characters_to_remove:
            stripped_density += char

    cleaned_density = stripped_density.lower()

    # If no density units given, assume units are correct
    if not cleaned_density:
        return lambda x: x

    # If density units identifiable, return corresponding conversion function
    else:
        for unit in DENSITY_CONVERSION:
            if unit in cleaned_density:
                return DENSITY_CONVERSION[unit]

    # If density units unidentifiable, raise ValueError
    raise ValueError(f"Unable to convert to units provided for density: {given_density}")

