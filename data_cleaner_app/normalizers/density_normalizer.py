import re
import string

from data_cleaner_app.normalizers.helpers import DENSITY_CONVERSION, get_temperature


def get_density(density: str) -> str:
    # If no density value provided, return empty string
    if not density:
        return ""

    temperature = get_temperature(density)

    # If only numerical density value given, assume units correct and return
    try:
        return str(float(density))
    except ValueError:
        pass

    # Attempt to parse value and units from beginning of density
    split_density_string = density.split()
    potential_unit_value = split_density_string[1:2]
    potential_numeric_value = split_density_string[0:1]

    if potential_unit_value and potential_unit_value:
        cleaned_potential_unit_value = re.sub(
            r"[\W_]+", "", str(potential_unit_value[0]).lower()
        )
        if cleaned_potential_unit_value in DENSITY_CONVERSION:
            conversion_function = DENSITY_CONVERSION[cleaned_potential_unit_value]
            try:
                return (
                    str(conversion_function(float(potential_numeric_value[0])))
                    + temperature
                )
            except Exception as ex:
                print(f"Unable to normalize density value {density}: {ex}")

    # If unableto parse density
    raise ValueError(f"Unable to parse temperature data from density value {density}")
