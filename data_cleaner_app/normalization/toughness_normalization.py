import re
import string
from typing import Callable, List, Dict

from data_cleaner_app.normalization.common import (
    get_temperature,
    get_value_range,
    get_initial_numeric_value,
    get_string_prior_to_substrings,
    clean_raw_string,
    get_unit_convertion_function,
    TEMPERATURE_CONVERSION,
    get_string_post_substrings,
    get_string_without_characters,
)
from data_cleaner_app.data_classes import NumericMaterial

TOUGHNESS_CONVERSION = {"mpam": lambda x: x}


def get_fracture_toughness(raw_toughness: str, warnings: List[Dict[str, str]]) -> str:

    is_common_case, toughness = clean_raw_string(raw_toughness)
    if is_common_case:
        return toughness

    value_substring = get_string_prior_to_substrings(toughness, ["@", "for"])
    temperature_substring = get_string_post_substrings(toughness, ["@", "for"])

    material = NumericMaterial(
        single_value=get_initial_numeric_value(s=value_substring, warnings=warnings),
        value_range=get_value_range(s=value_substring, warnings=warnings),
        temperature=get_initial_numeric_value(
            s=get_string_without_characters(
                s=temperature_substring, characters=["f", "°", "c", "k"]
            ),
            warnings=warnings,
        ),
        temperature_conversion=get_unit_convertion_function(
            s=temperature_substring,
            characters_to_remove=set(string.punctuation).union(string.digits),
            conversion_dict=TEMPERATURE_CONVERSION,
            safe_values=[],
        ),
        value_conversion=get_unit_convertion_function(
            s=value_substring,
            characters_to_remove=set(string.digits).union(string.punctuation),
            conversion_dict=TOUGHNESS_CONVERSION,
            safe_values=[],
        ),
    )

    return material.format()


# def get_toughness_unit_convertion_function(toughness: str) -> Callable[[float], float]:
#
#    # Strip puncation and whitespace characters (excluding "-") from toughness
#    characters_to_remove = (
#        set(string.punctuation).union(set(string.digits)).union(set(string.whitespace))
#    )
#
#    stripped_toughness = ""
#    for char in toughness:
#        if char not in characters_to_remove:
#            stripped_toughness += char
#
#    cleaned_toughness = stripped_toughness.lower()
#
#    safe_values = ["c", "k"]
#
#    # If no toughness units given, assume units are correct
#    if not cleaned_toughness or cleaned_toughness in safe_values:
#        return lambda x: x
#
#    # If toughness units identifiable, return corresponding conversion function
#    else:
#        for unit in TOUGHNESS_CONVERSION:
#            if unit in cleaned_toughness:
#                return TOUGHNESS_CONVERSION[unit]
#
#    # If toughness units unidentifiable, raise ValueError
#    raise ValueError(f"Unable to convert to units provided for toughness: {toughness}")
#
