import re
import string
from typing import Callable

from data_cleaner_app.normalizers.helpers import get_temperature, get_value_range, get_initial_numeric_value
from data_cleaner_app.data_classes import NumericMaterial

EXPANSION_CONVERSION = {
    "µmm": lambda x: x/1000000,
    "10-6": lambda x: x/1000000,
    "10-6°c": lambda x: x/1000000,
    "10-6°c": lambda x: x/1000000,
}


def get_coefficient_of_expansion(expansion: str) -> str:
    # If zero value given, assume units correct and return
    if expansion == "0":
        return "0"

    # If no expansion value provided, return empty string
    if not expansion:
        return ""

    # Attempt to split numerical value section from beginning of string, if 
    # divided by "µ" or "x" symbols. E.g. "7.00 µm/m-°C" or "10x10 -6 / ° C for 20C" 
    potential_numeric_section = expansion.lower().split("x")[0].split("µ")[0]

    material = NumericMaterial(
        single_value=get_initial_numeric_value(potential_numeric_section),
        value_range=get_value_range(potential_numeric_section),
        temperature=get_temperature(expansion),
        conversion=get_thermal_expansion_unit_convertion_function(expansion)
    )

    return material.format() 


def get_thermal_expansion_unit_convertion_function(expansion: str) -> Callable[[float],float]:

    # Strip puncation and whitespace characters (excluding "-") from expansion
    characters_to_remove = set(string.punctuation).difference({'-'}).union(string.whitespace)

    stripped_expansion = ""
    for char in expansion:
        if char not in characters_to_remove:
            stripped_expansion += char

    cleaned_expansion = stripped_expansion.lower()

    # If no density units given, assume units are correct
    if not cleaned_expansion:
        return lambda x: x

    # If density units identifiable, return corresponding conversion function
    else:
        for unit in EXPANSION_CONVERSION:
            if unit in cleaned_expansion:
                return EXPANSION_CONVERSION[unit]

    # If density units unidentifiable, raise ValueError
    raise ValueError(f"Unable to convert to units provided for expansion: {expansion}")

