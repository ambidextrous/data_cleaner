from typing import Optional, Tuple, List, Any, Dict, Set, Iterable, Callable
import re, string
import numpy as np

from data_cleaner_app.data_classes import NumericMaterial


TEMPERATURE_CONVERSION = {
    "°k": lambda x: -273.15,
    "k": lambda x: -273.15,
    "°c": lambda x: x,
    "c": lambda x: x,
    "°f": lambda x: (x - 32) * (5 / 9),
    "f": lambda x: (x - 32) * (5 / 9),
}


def get_value_range(s: str, warnings) -> Tuple[float, float]:
    """
    Extracts a range of numeric values from the beginning of a string, if divided by "to" or "-"
    E.g. "1.2 to 3.4" or "1.2-3.4" -> (1.2,3.4)
    """
    range_dividers = ["-", "to"]
    lowercase_s = s.lower()
    for divider in range_dividers:
        divided_by_range_list = lowercase_s.split(divider)
        if len(divided_by_range_list) > 1:
            try:
                bottom = convert_string_to_float(
                    s=divided_by_range_list[0].strip(), warnings=warnings
                )
                top = convert_string_to_float(
                    s=divided_by_range_list[1].split()[0].strip(), warnings=warnings
                )
                return bottom, top
            except (ValueError, IndexError):
                pass
    return tuple()


def get_initial_numeric_value(
    s: str, warnings: List[Dict[str, str]]
) -> Optional[float]:
    """
    Extracts the initial numberic value from a string
    E.g. ">6.3" or "<6.3" or "6.3°" or "6.3" -> 6.3
    """
    pruned_s = get_string_without_characters(s, [">", "<", "°"])
    lowercase_s = pruned_s.lower()
    split_string = lowercase_s.split()
    if split_string:
        try:
            return convert_string_to_float(s=split_string[0].strip(), warnings=warnings)
        except ValueError:
            pass
    return None


def get_string_prior_to_substrings(s: str, substrings: List[str]) -> str:
    """
    Extracts a substring prior to a list dividers:
    E.g.
    get_string_prior_to_substrings("abc@defg#hi",["@","#"]) -> "abc"
    """
    return_string = s.lower()
    for substring in substrings:
        try:
            return_string = return_string.split(substring)[0]
        except IndexError:
            raise ValueError(
                f"Unable to split string {s} on substring {substring} (substrings={substrings})"
            )
    return return_string


def get_string_post_substrings(s: str, substrings: List[str]) -> str:
    """
    Extracts a substring post a list dividers:
    E.g.
    get_string_post_substrings("abc@defg#hi", ["@","#"]) -> "hi"
    """
    return_string = s
    for substring in substrings:
        if substring in s:
            return_string = return_string.split(substring)[-1]
    if return_string == s:
        return ""
    else:
        return return_string


def get_string_without_characters(s: str, characters: Iterable[str]) -> str:
    """
    Gets a string minus given chacters
    E.g. get_string_without_character("abcde",["c","d"]) -> "abe"
    """
    return_string = ""
    for char in s:
        if char not in characters:
            return_string += char
    return return_string


def converts_to_float(anything: Any) -> bool:
    try:
        float(anything)
        return True
    except ValueError:
        return False


def clean_raw_string(raw_input: str) -> Tuple[bool, str]:
    """
    Carries out common checks on simple or falsy numeric values:
    - Returns (True, correct_output) if match found
    - Returns (False, raw_input) otherwise
    """
    if raw_input == np.nan or raw_input == "nan":
        return True, ""

    # Convert input to str
    s = str(raw_input).lower()

    # If zero value given, assume units correct and return
    if s == "0":
        return True, "0"

    # If no value provided, return empty string
    if not s:
        return True, ""

    # If single number given, assume units correct and return
    if converts_to_float(s):
        mat = NumericMaterial(
            single_value=float(s),
            value_range=tuple(),
            temperature=None,
            temperature_conversion=lambda x: x,
            value_conversion=lambda x: x,
        )
        return True, mat.format()

    return False, s


def get_unit_convertion_function(
    s: str,
    characters_to_remove: Iterable[str],
    conversion_dict: Dict[str, str],
    safe_values: Iterable[str],
) -> Callable[[float], float]:
    """
    
    """

    # Strip substrings to be removed from s
    stripped_string = ""
    for char in s:
        if char not in characters_to_remove:
            stripped_string += char

    cleaned_string = stripped_string.lower().strip()

    # If no units given or "safe value", assume units correct
    if not cleaned_string or cleaned_string in safe_values:
        return lambda x: x

    # If units identifiable, return corresponding conversion function
    else:
        for unit in conversion_dict:
            if unit in cleaned_string:
                return conversion_dict[unit]

    # If units non-identifiable, raise ValueError
    raise ValueError(
        f"Unable to find unit conversion function for string {s} (cleaned to {cleaned_string}) in conversion dict {conversion_dict} (safe_values={safe_values})"
    )


def convert_string_to_float(s: str, warnings: List[Dict[str, str]]) -> Optional[float]:
    # Attempt to convert to float
    try:
        value = float(s.strip())
        return value
    except ValueError:
        # Attempt to convert to float using "," decimal marker (and log warning)
        try:
            value = float(s.strip().replace(",", ""))
            message = f"Converted given value {s} to float value {value} using ',' thousands marker"
            warnings.append({"float_conversion_warning": message})
            return value
        except ValueError:
            pass
    raise ValueError(f"Unable to convert input {s} to float.")
