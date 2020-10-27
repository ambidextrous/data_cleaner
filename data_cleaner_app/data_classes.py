from dataclasses import dataclass
import numpy as np


@dataclass
class MaterialAttribute:
    name: str
    value_range: tuple
    temperature: int = None


@dataclass
class NumericMaterial:
    single_value: float
    value_range: tuple
    temperature: float
    temperature_conversion: callable
    value_conversion: callable

    def _format_float(self, number: float) -> str:
        """
        Formats float to string representation

        float(0.000001) -> '1e-06'

        _format_float(0.000001) -> '0.000001'

        Removes final decimal marker from non-decimal numbers

        np.format_float_positional(8) -> '8.'

        _format_float(8) -> '8'

        """
        stringified_float = str(np.format_float_positional(number))
        if stringified_float.endswith("."):
            return stringified_float[:-1]
        return stringified_float

    def format(self):
        if self.temperature is not None:
            temp_representation = (
                f";{self._format_float(self.temperature_conversion(self.temperature))}"
            )
        else:
            temp_representation = ""
        if (self.single_value is None) and (not self.value_range):
            raise ValueError("Unable to parse value data from numeric material")
        elif self.value_range:
            bottom = self._format_float(self.value_conversion(self.value_range[0]))
            top = self._format_float(self.value_conversion(self.value_range[1]))
            return f"{bottom},{top}{temp_representation}"
        else:
            val = self._format_float(self.value_conversion(self.single_value))
            return f"{val}{temp_representation}"
