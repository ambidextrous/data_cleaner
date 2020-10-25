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
    conversion: callable

    def format(self):
        if self.temperature is not None:
            temp_representation = f";{round(self.temperature) if str(self.temperature).endswith('.0') else np.format_float_positional(self.temperature)}"
        else:
            temp_representation = ""
        if (self.single_value is None) and (not self.value_range):
            raise ValueError("Unable to parse value data from numeric material")
        elif self.value_range:
            bottom = str(
                np.format_float_positional(self.conversion(self.value_range[0]))
            )
            if bottom.endswith("."):
                bottom = bottom[:-1]
            top = str(np.format_float_positional(self.conversion(self.value_range[1])))
            if top.endswith("."):
                top = top[:-1]
            return f"{bottom},{top}{temp_representation}"
        else:
            val = np.format_float_positional(self.conversion(self.single_value))
            return f"{val}{temp_representation}"
