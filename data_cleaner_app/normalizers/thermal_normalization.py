import re
import string
from typing import Callable

from data_cleaner_app.normalizers.helpers import (
    get_temperature,
    get_value_range,
    get_initial_numeric_value,
    get_string_prior_to_substrings,
    get_string_post_substrings,
    converts_to_float,
    clean_raw_string,
)
from data_cleaner_app.data_classes import NumericMaterial

CONDUCTIVITY_CONVERSION = {"wmk": lambda x: x}


def get_thermal_conductivity(raw_conductivity: str) -> str:

    is_common_case, conductivity = clean_raw_string(raw_conductivity)
    if is_common_case:
        return conductivity

    potential_numeric_section = get_string_prior_to_substrings(
        conductivity, ["@", "for"]
    )
    potential_temperature_section = get_string_post_substrings(
        conductivity, ["@", "for"]
    )

    material = NumericMaterial(
        single_value=get_initial_numeric_value(potential_numeric_section),
        value_range=get_value_range(potential_numeric_section),
        temperature=get_temperature(potential_temperature_section),
        conversion=get_conductivity_unit_convertion_function(potential_numeric_section),
    )

    return material.format()


def get_conductivity_unit_convertion_function(
    conductivity: str
) -> Callable[[float], float]:

    # Strip puncation and whitespace characters (excluding "-") from toughness
    characters_to_remove = (
        set(string.punctuation).union(set(string.digits)).union(set(string.whitespace))
    )

    stripped_conductivity = ""
    for char in conductivity:
        if char not in characters_to_remove:
            stripped_conductivity += char

    cleaned_conductivity = stripped_conductivity.lower()

    # If no magnetic units given, assume units are correct
    if not cleaned_conductivity or cleaned_conductivity in safe_values:
        return lambda x: x

    # If magnetic units identifiable, return corresponding conversion function
    else:
        for unit in CONDUCTIVITY_CONVERSION:
            if unit in cleaned_conductivity:
                return CONDUCTIVITY_CONVERSION[unit]

    # If magnetic units unidentifiable, raise ValueError
    raise ValueError(
        f"Unable to convert to units provided for thermal conductivity: {conductivity}"
    )
