from dataclasses import dataclass
import numpy as np


@dataclass
class NumericMaterial:
    """
    Dataclass representing a material with numerical attributes

    single_value: a single value, e.g. 2.45
    value_range: a range of value, e.g. 2.3-2.5
    temperature: a temperature, e.g. 3.9
    temperature_conversion: a transformation function to be applied to a temperature value to convert it to the correct format, e.g. x-273.15
    vaue_conversion: a transformation function to be applied to a value for it to be converted to the correct format, e.g. x*1000

    """
    single_value: float
    value_range: tuple
    temperature: float
    temperature_conversion: callable
    value_conversion: callable

    def _format_float(self, number: float) -> str:
        """
        Formats float to specified string representation:

        BAD: float(0.000001) -> '1e-06'

        GOOD: _format_float(0.000001) -> '0.000001'

        Removes final decimal marker from non-decimal numbers

        BAD: np.format_float_positional(8) -> '8.'

        GOOD: _format_float(8) -> '8'
        """
        stringified_float = str(np.format_float_positional(number))
        if stringified_float.endswith("."):
            return stringified_float[:-1]
        return stringified_float

    def format(self):
        """
        Format numberic material correctly for output to spreadsheet:

        E.g.
        -> 2 - If only single value given
        -> 2-3 - If range of values give
        -> 2;5 - If value and temperature given
        -> 2-3;5 - If range of values and temperature given
        """
        # If temperature given, add at end of output, separated by ";"
        if self.temperature is not None:
            temp_representation = (
                f";{self._format_float(self.temperature_conversion(self.temperature))}"
            )
        else:
            temp_representation = ""
        # If no value given, raise error
        if (self.single_value is None) and (not self.value_range):
            raise ValueError("Unable to parse value data from numeric material")
        # If range of values given, add both, e.g. "4.3-4.5"
        elif self.value_range:
            bottom = self._format_float(self.value_conversion(self.value_range[0]))
            top = self._format_float(self.value_conversion(self.value_range[1]))
            return f"{bottom},{top}{temp_representation}"
        # If only single value given, add it, e.g. "4.3"
        else:
            val = self._format_float(self.value_conversion(self.single_value))
            return f"{val}{temp_representation}"
