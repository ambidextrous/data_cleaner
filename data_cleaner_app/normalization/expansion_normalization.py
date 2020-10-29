import re
import string
from typing import Callable, List, Dict

from data_cleaner_app.normalization.common import (
    get_value_range,
    get_initial_numeric_value,
    get_string_prior_to_substrings,
    get_string_post_substrings,
    get_unit_convertion_function,
    clean_raw_string,
    TEMPERATURE_CONVERSION,
    get_string_without_characters,
)
from data_cleaner_app.data_classes import NumericMaterial

EXPANSION_CONVERSION = {
    "µmm": lambda x: x / 1_000_000,
    "µm/m": lambda x: x / 1_000_000,
    "10-6": lambda x: x / 1_000_000,
    "10-6°c": lambda x: x / 1_000_000,
    "10-6°c": lambda x: x / 1_000_000,
}


def get_coefficient_of_expansion(
    raw_expansion: str, warnings: List[Dict[str, str]]
) -> str:
    """
    Converts a raw input string into a correctly formatted output string.
    First parses data from input by passing transformed versions of the
    raw input to the constructor of a NumericalMaterial object, then calls
    the .format() method of that object to correctly format output.

    Adjustments to field normalization should be made by altering the parameters 
    passed to the NumericalMaterial constructor here.
    """

    is_common_case, expansion = clean_raw_string(raw_expansion)
    if is_common_case:
        return expansion

    # Attempt to split numerical value section from beginning of string, if
    # divided by "µ" or "x" symbols. E.g. "7.00 µm/m-°C" or "10x10 -6 / ° C for 20C"
    value_substring = get_string_prior_to_substrings(expansion, ["x", "µ", "for", "@"])
    temperature_substring = get_string_post_substrings(expansion, ["for", "@"])
    unit_substring = get_string_prior_to_substrings(
        s=expansion, substrings=["for", "@"]
    )

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
            characters_to_remove=set(string.digits).union(string.punctuation),
            conversion_dict=TEMPERATURE_CONVERSION,
            safe_values=[],
        ),
        value_conversion=get_unit_convertion_function(
            s=expansion,
            characters_to_remove=set(string.whitespace),
            conversion_dict=EXPANSION_CONVERSION,
            safe_values=[],
        ),
    )

    return material.format()
