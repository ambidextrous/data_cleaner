import re
import string
from typing import Callable, List, Dict

from data_cleaner_app.normalization.common import (
    get_value_range,
    get_initial_numeric_value,
    get_string_prior_to_substrings,
    get_unit_convertion_function,
    converts_to_float,
    clean_raw_string,
    TEMPERATURE_CONVERSION,
)
from data_cleaner_app.data_classes import NumericMaterial

MAGNETIC_CONVERSION = {}


def get_magnetic_susceptibility(
    raw_magnetic: str, warning: List[Dict[str, str]]
) -> str:
    """
    Converts a raw input string into a correctly formatted output string.
    First parses data from input by passing transformed versions of the
    raw input to the constructor of a NumericalMaterial object, then calls
    the .format() method of that object to correctly format output.

    Adjustments to field normalization should be made by altering the parameters 
    passed to the NumericalMaterial constructor here.
    """

    is_common_case, magnetic = clean_raw_string(raw_magnetic)
    if is_common_case:
        return magnetic

    potential_numeric_section = get_string_prior_to_substrings(magnetic, ["@", "for"])
    temperature_substring = get_string_post_substrings(magnetic, ["for", "@"])

    material = NumericMaterial(
        single_value=get_initial_numeric_value(potential_numeric_section, warnings),
        value_range=get_value_range(potential_numeric_section, warnings),
        temperature=get_initial_numeric_value(temperature_substring),
        temperature_conversion=get_unit_convertion_function(
            s=temperature_substring,
            characters_to_remove=set(string.digits).union(string.punctuation),
            conversion_dict=TEMPERATURE_CONVERSION,
            safe_values=[],
        ),
        value_conversion=get_unit_convertion_function(
            s=potential_numeric_section,
            characters_to_remove=[],
            conversion_dict=MAGNETIC_CONVERSION,
            safe_values=[],
        ),
    )

    return material.format()
