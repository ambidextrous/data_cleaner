import re
import string
from typing import Callable

from data_cleaner_app.normalizers.helpers import (
    get_temperature,
    get_value_range,
    get_initial_numeric_value,
    get_string_prior_to_substrings,
    converts_to_float,
    clean_raw_string,
)
from data_cleaner_app.data_classes import NumericMaterial

MAGNETIC_CONVERSION = {}


def get_magnetic_susceptibility(raw_magnetic: str) -> str:

    is_common_case, magnetic = clean_raw_string(raw_magnetic)
    if is_common_case:
        return magnetic

    potential_numeric_section = get_string_prior_to_substrings(magnetic, ["@", "for"])

    material = NumericMaterial(
        single_value=get_initial_numeric_value(potential_numeric_section),
        value_range=get_value_range(potential_numeric_section),
        temperature=get_temperature(magnetic),
        conversion=get_magnetic_unit_convertion_function(magnetic),
    )

    return material.format()


def get_magnetic_unit_convertion_function(magnetic: str) -> Callable[[float], float]:

    # Strip puncation and whitespace characters (excluding "-") from toughness
    characters_to_remove = (
        set(string.punctuation).union(set(string.digits)).union(set(string.whitespace))
    )

    stripped_magnetic = ""
    for char in magnetic:
        if char not in characters_to_remove:
            stripped_magnetic += char

    cleaned_magnetic = stripped_magnetic.lower()

    safe_values = ["c", "k"]

    # If no magnetic units given, assume units are correct
    if not cleaned_magnetic or cleaned_magnetic in safe_values:
        return lambda x: x

    # If magnetic units identifiable, return corresponding conversion function
    else:
        for unit in MAGNETIC_CONVERSION:
            if unit in cleaned_magnetic:
                return MAGNETIC_CONVERSION[unit]

    # If magnetic units unidentifiable, raise ValueError
    raise ValueError(
        f"Unable to convert to units provided for magnetic susceptibility: {magnetic}"
    )
