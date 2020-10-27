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


def get_temperature(s: str) -> Optional[float]:
    potential_temp_values = [s.split("@"), s.split("for")]

    for potential_temp_value in potential_temp_values:
        sign_factor = 1
        if potential_temp_value[-1:]:
            if "-" in potential_temp_value[-1:][0]:
                sign_factor = -1
            try:
                return float(potential_temp_value[-1:][0])
            except Exception:
                pass
            alpha_numeric_only_value = re.sub(
                r"[\W_]+", "", potential_temp_value[-1:][0].lower()
            )
            if "c" in alpha_numeric_only_value or "k" in alpha_numeric_only_value:
                try:
                    return (
                        float(alpha_numeric_only_value.replace("c", "")) * sign_factor
                    )
                except Exception:
                    pass
            elif "f" in alpha_numeric_only_value:
                try:
                    return (
                        (float(alpha_numeric_only_value.replace("f", "")) - 32)
                        * 5
                        / 9
                        * sign_factor
                    )
                except Exception:
                    pass

    return None


def get_value_range(s: str) -> Tuple[float, float]:
    range_dividers = ["-", "to"]
    lowercase_s = s.lower()
    for divider in range_dividers:
        divided_by_range_list = lowercase_s.split(divider)
        if len(divided_by_range_list) > 1:
            try:
                bottom = float(divided_by_range_list[0].strip())
                top = float(divided_by_range_list[1].split()[0].strip())
                return (bottom, top)
            except (ValueError, IndexError):
                try:
                    bottom = float(divided_by_range_list[0].strip().replace(",", "."))
                    top = float(
                        divided_by_range_list[1].split()[0].strip().replace(",", ".")
                    )
                    return (bottom, top)
                except (ValueError, IndexError):
                    pass
    return tuple()


def get_initial_numeric_value(
    s: str, warnings: List[Dict[str, str]]
) -> Optional[float]:
    pruned_s = get_string_without_characters(s, [">", "<", "°"])
    lowercase_s = pruned_s.lower()
    split_string = lowercase_s.split()
    print(f"split_string={split_string}")
    if split_string:
        try:
            return convert_string_to_float(
                input=split_string[0].strip(), warnings=warnings
            )
        except ValueError:
            pass
    return None


def get_string_prior_to_substrings(s: str, substrings: List[str]) -> str:
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
    print(f"s={s}")
    return_string = s
    for substring in substrings:
        if substring in s:
            print(f"substring={substring}")
            try:
                return_string = return_string.split(substring)[-1]
                print(f"return_string={return_string}")
            except IndexError:
                raise ValueError(
                    f"Unable to split string {s} on substring {substring} (substrings={substrings})"
                )
    if return_string == s:
        return ""
    else:
        return return_string


def get_string_without_characters(s: str, characters: Iterable[str]) -> str:
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
            conversion=lambda x: x,
        )
        return True, mat.format()

    return False, s


def get_unit_convertion_function(
    s: str,
    characters_to_remove: Iterable[str],
    conversion_dict: Dict[str, str],
    safe_values: Iterable[str],
) -> Callable[[float], float]:

    # Strip substrings to be removed from s
    stripped_string = ""
    for char in s:
        if char not in characters_to_remove:
            stripped_string += char

    cleaned_string = stripped_string.lower()

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


def convert_string_to_float(
    input: str, warnings: List[Dict[str, str]]
) -> Optional[float]:
    # Attempt to convert to float
    try:
        value = float(input.strip())
        return value
    except ValueError:
        # Attempt to convert to float using "," decimal marker (and log warning)
        try:
            value = float(input.strip().replace(",", ""))
            message = f"Converted given value {input} to float value {value} using ',' thousands marker"
            warnings.append({"float_conversion_warning": message})
            # TODO: Add warning logging
            return value
        except ValueError:
            pass
    raise ValueError(f"Unable to convert input {input} to float.")
