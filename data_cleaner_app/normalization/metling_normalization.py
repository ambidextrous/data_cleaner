import re
import string
from typing import Callable, List, Dict

from data_cleaner_app.normalization.common import (
    get_value_range,
    get_initial_numeric_value,
    get_string_prior_to_substrings,
    get_unit_convertion_function,
    clean_raw_string,
    TEMPERATURE_CONVERSION,
)
from data_cleaner_app.data_classes import NumericMaterial


def get_metling_point(raw_melting_point: str, warnings: List[Dict[str, str]]) -> str:

    is_common_case, melting_point = clean_raw_string(raw_melting_point)
    if is_common_case:
        return melting_point

    material = NumericMaterial(
        single_value=get_initial_numeric_value(s=melting_point, warnings=warnings),
        value_range=get_value_range(melting_point, []),
        temperature=None,
        value_conversion=get_unit_convertion_function(
            s=melting_point,
            characters_to_remove=set(string.printable).difference({"k", "c", "f"}),
            conversion_dict=TEMPERATURE_CONVERSION,
            safe_values=[],
        ),
        temperature_conversion=lambda x: x,
    )

    return material.format()
