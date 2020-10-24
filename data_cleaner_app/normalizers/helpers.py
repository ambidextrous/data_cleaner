from typing import Optional
import re, string


DENSITY_CONVERSION = {
    "gc3": lambda x: x,
    "gcc": lambda x: x,
    "kgm3": lambda x: x * 0.001,
    "kgmc": lambda x: x * 0.001,
    "kgl": lambda x: x,
    "gml": lambda x: x,
    "tm3": lambda x: x,
    "tmc": lambda x: x,
}

TEMPERATURE_CONVERSION = {"c": lambda x: x, "f": lambda x: (x - 32) * 5 / 9}


def get_temperature(s: str) -> str:
    potential_temp_values = [s.split("@"), s.split("for")]

    for potential_temp_value in potential_temp_values:
        sign_factor = 1
        if potential_temp_value[-1:]:
            if "-" in potential_temp_value[-1:][0]:
                sign_factor = -1
            try:
                return ";" + str(float(potential_temp_value[-1:][0]))
            except Exception:
                pass
            alpha_numeric_only_value = re.sub(
                r"[\W_]+", "", potential_temp_value[-1:][0].lower()
            )
            if "c" in alpha_numeric_only_value:
                try:
                    return ";" + str(
                        float(alpha_numeric_only_value.replace("c", "")) * sign_factor
                    )
                except Exception:
                    pass
            elif "f" in alpha_numeric_only_value:
                try:
                    return ";" + str(
                        (float(alpha_numeric_only_value.replace("f", "")) - 32)
                        * 5
                        / 9
                        * sign_factor
                    )
                except Exception:
                    pass

    return ""
