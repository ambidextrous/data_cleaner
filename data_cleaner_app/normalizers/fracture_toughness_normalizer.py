import re
import string
from typing import Callable

from data_cleaner_app.normalizers.helpers import (
    get_temperature,
    get_value_range,
    get_initial_numeric_value,
    get_string_prior_to_substrings,
    check_common_cases,
)
from data_cleaner_app.data_classes import NumericMaterial

TOUGHNESS_CONVERSION = {"mpam": lambda x: x}


def get_fracture_toughness(toughness: str) -> str:

    is_common_case, common_case_result = check_common_cases(toughness)
    if is_common_case:
        return common_case_result

    potential_numeric_section = get_string_prior_to_substrings(toughness, ["@", "for"])

    material = NumericMaterial(
        single_value=get_initial_numeric_value(potential_numeric_section),
        value_range=get_value_range(potential_numeric_section),
        temperature=get_temperature(toughness),
        conversion=get_toughness_unit_convertion_function(toughness),
    )

    return material.format()


def get_toughness_unit_convertion_function(toughness: str) -> Callable[[float], float]:

    # Strip puncation and whitespace characters (excluding "-") from toughness
    characters_to_remove = (
        set(string.punctuation).union(set(string.digits)).union(set(string.whitespace))
    )

    stripped_toughness = ""
    for char in toughness:
        if char not in characters_to_remove:
            stripped_toughness += char

    cleaned_toughness = stripped_toughness.lower()

    safe_values = ["c", "k"]

    # If no toughness units given, assume units are correct
    if not cleaned_toughness or cleaned_toughness in safe_values:
        return lambda x: x

    # If toughness units identifiable, return corresponding conversion function
    else:
        for unit in TOUGHNESS_CONVERSION:
            if unit in cleaned_toughness:
                return TOUGHNESS_CONVERSION[unit]

    print(f"cleaned_toughness={cleaned_toughness}")
    # If toughness units unidentifiable, raise ValueError
    raise ValueError(f"Unable to convert to units provided for toughness: {toughness}")
