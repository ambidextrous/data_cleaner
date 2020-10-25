from dataclasses import dataclass


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
            temp_representation = f";{self.temperature}"
        else:
            temp_representation = ""
        if (self.single_value is None) and (not self.value_range):
            raise ValueError("Unable to parse value data from numeric material")
        elif self.value_range:
            return f"{self.conversion(self.value_range[0])},{self.conversion(self.value_range[1])}{temp_representation}"
        else:
            return f"{self.conversion(self.single_value)}{temp_representation}"
