import re
import string
from typing import Callable, List

from data_cleaner_app.normalization.common import (
    get_value_range,
    get_initial_numeric_value,
    clean_raw_string,
    get_unit_convertion_function,
    get_string_prior_to_substrings,
    get_string_post_substrings,
    get_string_without_characters,
    TEMPERATURE_CONVERSION,
)
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


def get_density(raw_density: str, warnings: List) -> str:

    is_common_case, density = clean_raw_string(raw_density)
    if is_common_case:
        return density

    temperature_substring = get_string_post_substrings(
        s=density, substrings=["@", "for"]
    )
    value_substring = get_string_prior_to_substrings(s=density, substrings=["@", "for"])

    material = NumericMaterial(
        single_value=get_initial_numeric_value(s=value_substring, warnings=warnings),
        value_range=get_value_range(value_substring, warnings),
        value_conversion=get_unit_convertion_function(
            s=density,
            characters_to_remove=set(string.digits).union(string.punctuation),
            conversion_dict=DENSITY_CONVERSION,
            safe_values=[],
        ),
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
    )
    print(f"material={material}")

    return material.format()
