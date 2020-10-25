from typing import Optional, Tuple, List
import re, string


TEMPERATURE_CONVERSION = {"c": lambda x: x, "f": lambda x: (x - 32) * 5 / 9}


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
            print(f"divided_by_range_list={divided_by_range_list}")
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


def get_initial_numeric_value(s: str) -> Optional[float]:
    pruned_s = get_string_without_substrings(s, [">", "<"])
    lowercase_s = pruned_s.lower()
    split_string = lowercase_s.split()
    if split_string:
        try:
            value = float(split_string[0].strip())
            return value
        except ValueError:
            try:
                value = float(split_string[0].strip().replace(",", "."))
                return value
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
    print(f"return_string={return_string}")
    return return_string


def get_string_without_substrings(s: str, substrings: List[str]) -> str:
    return_string = ""
    for char in s:
        if char not in substrings:
            return_string += char
    return return_string
